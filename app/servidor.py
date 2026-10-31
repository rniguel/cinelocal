# -*- coding: utf-8 -*-
"""
Servidor local leve CineLocal com streaming de alta velocidade (HTTP 206 Range Requests)
e integração com VLC para reprodução de formatos avançados (Dolby TrueHD, AC3 5.1, DTS).
"""

import http.server
import socketserver
import os
import sys
import socket
import webbrowser
import json
import urllib.parse
import urllib.request
import subprocess
import re
import shutil
import time
import threading
import queue
from datetime import datetime

PORT = 8000
APP_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_DIR = os.path.dirname(APP_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from atualizar_catalogo import build_catalog, parse_srt

PORTABLE_VLC = os.path.join(APP_DIR, "vlc", "vlc.exe")
SYSTEM_VLC = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

AUDIO_CACHE = {}
AUDIO_INFO_CACHE = {}
_CLIENT_ACTIVITY_CACHE = {}

def should_log_activity(key, window_seconds=12):
    """Evita flooding de logs em requisições repetidas num intervalo curto."""
    now = time.time()
    last = _CLIENT_ACTIVITY_CACHE.get(key, 0)
    if now - last > window_seconds:
        _CLIENT_ACTIVITY_CACHE[key] = now
        return True
    return False

def log_event(icon, tag, message):
    """Exibe logs limpos e padronizados com timestamp e emojis."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {icon}  {tag:<13} {message}")

def safe_resolve_media_path(base_dir, req_path):
    """
    Resolve com segurança um caminho de mídia relativo garantindo que ele
    permaneça estritamente contido dentro do diretório 'media' (proteção contra Path Traversal).
    Retorna o caminho canônico absoluto ou None se for inválido/malicioso.
    """
    if not req_path:
        return None
    try:
        unquoted = urllib.parse.unquote(str(req_path)).strip()
        normalized = unquoted.replace('\\', '/')
        parts = [p for p in normalized.split('/') if p and p != '.']
        
        # Remove prefixo legítimo '../' gerado pelo frontend em /app/
        if parts and parts[0] == '..':
            parts.pop(0)
            
        # Todo caminho de mídia deve obrigatoriamente iniciar com a pasta 'media'
        if not parts or parts[0] != 'media':
            return None
            
        # Bloqueia se houver '..' ou pontos extras/colons em qualquer segmento
        for p in parts:
            if '..' in p or ':' in p:
                return None
                
        safe_rel = os.path.join(*parts)
        real_media_base = os.path.realpath(os.path.join(base_dir, 'media'))
        full_path = os.path.realpath(os.path.abspath(os.path.join(base_dir, safe_rel)))
        
        # Garante que o caminho final resolvido está estritamente dentro de media/
        if full_path == real_media_base or full_path.startswith(real_media_base + os.sep):
            return full_path
        return None
    except Exception as e:
        log_event("⚠️", "SEGURANÇA", f"Tentativa de path traversal rejeitada: {req_path} ({e})")
        return None

def get_ffmpeg_bin():
    """Localiza o FFmpeg na pasta app/bin, no PATH do sistema ou em caminhos padroes."""
    local_bin = os.path.join(APP_DIR, "bin", "ffmpeg.exe")
    if os.path.exists(local_bin):
        return local_bin
    system_bin = shutil.which("ffmpeg")
    if system_bin:
        return system_bin
    for candidate in [
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe")
    ]:
        if os.path.exists(candidate):
            return candidate
    return None

def get_best_audio_stream(movie_path):
    if movie_path in AUDIO_CACHE:
        return AUDIO_CACHE[movie_path]
    ffmpeg_bin = get_ffmpeg_bin()
    if not ffmpeg_bin:
        return "1"
    try:
        res = subprocess.run([ffmpeg_bin, "-i", movie_path], capture_output=True, text=True, encoding="utf-8", errors="ignore")
        lines = res.stderr.split("\n")
        por_streams = []
        all_audio_streams = []
        for l in lines:
            m = re.search(r"Stream #0:(\d+)(?:\(([a-zA-Z]+)\))?.*?: Audio:", l)
            if m:
                idx = m.group(1)
                lang = (m.group(2) or "und").lower()
                all_audio_streams.append(idx)
                if lang in ("por", "pob", "pt", "bra"):
                    por_streams.append(idx)
        best = por_streams[0] if por_streams else (all_audio_streams[0] if all_audio_streams else "1")
        AUDIO_CACHE[movie_path] = best
        return best
    except Exception:
        return "1"

def get_audio_streams_info(movie_path):
    """Detecta as faixas de áudio disponíveis no vídeo via FFmpeg e calcula a duração total em segundos."""
    if movie_path in AUDIO_INFO_CACHE:
        return AUDIO_INFO_CACHE[movie_path]
    ffmpeg_bin = get_ffmpeg_bin()
    if not ffmpeg_bin or not os.path.exists(movie_path):
        return {"streams": [], "duration": 0}
    try:
        res = subprocess.run(
            [ffmpeg_bin, "-i", movie_path],
            capture_output=True, text=True, encoding="utf-8", errors="ignore"
        )
        duration_sec = 0.0
        dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", res.stderr)
        if dur_match:
            h, m, s = int(dur_match.group(1)), int(dur_match.group(2)), float(dur_match.group(3))
            duration_sec = round(h * 3600 + m * 60 + s, 2)

        streams = []
        for line in res.stderr.split("\n"):
            m = re.search(r"Stream #0:(\d+)(?:\(([a-zA-Z]+)\))?.*?: Audio: (.*)", line)
            if m:
                idx = int(m.group(1))
                lang = (m.group(2) or "und").lower()
                details = m.group(3).strip()
                
                if lang in ("por", "pob", "pt", "bra"):
                    lang_label = "Português (Dublado)"
                elif lang in ("eng", "en"):
                    lang_label = "Inglês (Original)"
                elif lang in ("spa", "es"):
                    lang_label = "Espanhol"
                elif lang in ("jpn", "ja"):
                    lang_label = "Japonês"
                elif lang in ("fra", "fr"):
                    lang_label = "Francês"
                else:
                    lang_label = f"Áudio ({lang.upper()})"
                
                channels = "Estéreo"
                if "5.1" in details or "6 channels" in details:
                    channels = "5.1 Surround"
                elif "7.1" in details or "8 channels" in details:
                    channels = "7.1 Surround"
                
                streams.append({
                    "index": idx,
                    "language": lang,
                    "label": f"{lang_label} • {channels}",
                    "details": details
                })
        result = {"streams": streams, "duration": duration_sec}
        if duration_sec > 0:
            AUDIO_INFO_CACHE[movie_path] = result
        return result
    except Exception as e:
        print(f"Erro ao extrair audio_info: {e}")
        return {"streams": [], "duration": 0}

def download_online_subtitle(video_rel, query_title, imdb_id=None, season=None, episode=None):
    """Busca e baixa automaticamente legendas em pt-BR via OpenSubtitles/Cinemeta."""
    full_video_path = safe_resolve_media_path(MOVIES_DIR, video_rel)
    if not full_video_path or not os.path.exists(full_video_path):
        return {"success": False, "message": "Arquivo de vídeo não encontrado no disco"}
    
    target_dir = os.path.dirname(full_video_path)
    base_name = os.path.splitext(os.path.basename(full_video_path))[0]
    sub_filename = f"{base_name}.pt.srt"
    sub_path = os.path.join(target_dir, sub_filename)

    # 1. Tenta identificar IMDb ID caso não venha informado ou venha como URL
    if imdb_id:
        m = re.search(r'(tt\d+)', str(imdb_id))
        imdb_id = m.group(1) if m else None

    if not imdb_id:
        try:
            clean_title = re.sub(r'\s*\(\d{4}\).*', '', query_title).strip()
            search_type = "series" if (season is not None and episode is not None) else "movie"
            search_url = f"https://v3-cinemeta.strem.io/catalog/{search_type}/top/search={urllib.parse.quote(clean_title)}.json"
            req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (CineLocal/2.4)'})
            with urllib.request.urlopen(req, timeout=6) as res:
                data = json.loads(res.read().decode('utf-8'))
                metas = data.get('metas', [])
                if metas:
                    imdb_id = metas[0].get('id')
        except Exception as e:
            print(f"Erro ao buscar IMDb ID: {e}")

    if not imdb_id:
        return {"success": False, "status": "error", "message": f"Não foi possível identificar '{query_title}' online para buscar legendas"}

    # 2. Busca legendas no OpenSubtitles v3
    try:
        if season is not None and episode is not None:
            sub_query_id = f"{imdb_id}:{season}:{episode}"
            sub_url = f"https://opensubtitles-v3.strem.io/subtitles/series/{sub_query_id}.json"
        else:
            sub_url = f"https://opensubtitles-v3.strem.io/subtitles/movie/{imdb_id}.json"
        
        req = urllib.request.Request(sub_url, headers={'User-Agent': 'Mozilla/5.0 (CineLocal/2.4)'})
        with urllib.request.urlopen(req, timeout=8) as res:
            sub_data = json.loads(res.read().decode('utf-8'))
            subs = sub_data.get('subtitles', [])
            
        por_subs = [s for s in subs if s.get('lang') in ('pob', 'por', 'pt-br', 'pt')]
        if not por_subs:
            return {"success": False, "status": "error", "message": "Nenhuma legenda em português encontrada online"}
        
        # Pega a melhor legenda em português
        download_url = por_subs[0].get('url')
        if not download_url:
            return {"success": False, "status": "error", "message": "URL de download da legenda indisponível"}
        
        # Baixa a legenda
        req_dl = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0 (CineLocal/2.4)'})
        with urllib.request.urlopen(req_dl, timeout=10) as dl_res:
            content_bytes = dl_res.read()
            text_str = content_bytes.decode('utf-8', errors='ignore')
            with open(sub_path, 'w', encoding='utf-8-sig') as f:
                f.write(text_str)
        
        rel_sub_path = os.path.relpath(sub_path, MOVIES_DIR).replace('\\', '/')
        if not rel_sub_path.startswith('../'):
            rel_sub_path = f"../{rel_sub_path}"
        
        cues = parse_srt(text_str)
        log_event("📥", "LEGENDA", f"Legenda pt-BR baixada com sucesso para '{base_name}'")
        sub_info = {
            "filename": sub_filename,
            "name": sub_filename,
            "path": rel_sub_path,
            "relative_path": rel_sub_path,
            "label": "Português (Brasil)",
            "cues": cues
        }
        return {
            "success": True,
            "status": "ok",
            "filename": sub_filename,
            "path": rel_sub_path,
            "relative_path": rel_sub_path,
            "label": "Português (Brasil)",
            "cues": cues,
            "subtitle": sub_info
        }
    except Exception as e:
        print(f"Erro ao baixar legenda: {e}")
        return {"success": False, "status": "error", "message": f"Erro ao baixar legenda: {e}"}

DATA_DIR = os.path.join(APP_DIR, "data")
USER_STATE_FILE = os.path.join(DATA_DIR, "user_state.json")
USER_STATE_LOCK = threading.Lock()

class RemoteControllerHub:
    """Distribui comandos do controle remoto virtual via Server-Sent Events (SSE) e polling."""
    def __init__(self):
        self.listeners = []
        self.lock = threading.Lock()
        self.history = []

    def subscribe(self):
        q = queue.Queue(maxsize=40)
        with self.lock:
            self.listeners.append(q)
        return q

    def unsubscribe(self, q):
        with self.lock:
            if q in self.listeners:
                self.listeners.remove(q)

    def dispatch(self, action, payload=None):
        event = {
            "action": action,
            "payload": payload or {},
            "id": int(time.time() * 1000)
        }
        with self.lock:
            self.history.append(event)
            if len(self.history) > 60:
                self.history.pop(0)
            for q in list(self.listeners):
                try:
                    q.put_nowait(event)
                except queue.Full:
                    pass
        return event

    def get_events_since(self, since_id):
        with self.lock:
            return [e for e in self.history if e["id"] > since_id]

REMOTE_HUB = RemoteControllerHub()

CINEMA_CACHE_FILE = os.path.join(DATA_DIR, "cinema_releases.json")
TMDB_API_KEY = "1cf50e6248dc270629e802686245c2c8"

def load_user_state():
    """Carrega o progresso e favoritos globais sincronizados entre dispositivos com thread-lock."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    with USER_STATE_LOCK:
        if os.path.exists(USER_STATE_FILE):
            try:
                with open(USER_STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        data = {}
                    if "watchProgress" not in data:
                        data["watchProgress"] = {}
                    if "favorites" not in data:
                        data["favorites"] = []
                    if "watchedList" not in data:
                        data["watchedList"] = {}
                    return data
            except Exception:
                pass
        return {"watchProgress": {}, "favorites": [], "watchedList": {}}

def get_cinema_releases():
    """Obtém lançamentos de cinema e filmes em cartaz (com cache local de 6h)."""
    now = time.time()
    if os.path.exists(CINEMA_CACHE_FILE):
        try:
            mtime = os.path.getmtime(CINEMA_CACHE_FILE)
            if now - mtime < 21600:  # 6 horas
                with open(CINEMA_CACHE_FILE, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                    if cached.get("releases"):
                        return cached
        except Exception:
            pass

    # Busca no TMDb oficial com região Brasil e idioma pt-BR
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=pt-BR&page=1&region=BR"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CineLocal/2.0"})
        with urllib.request.urlopen(req, timeout=12) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
            results = data.get("results", [])
            clean_results = []
            for m in results:
                poster_path = m.get("poster_path")
                backdrop_path = m.get("backdrop_path")
                clean_results.append({
                    "id": m.get("id"),
                    "title": m.get("title") or m.get("original_title", "Sem título"),
                    "originalTitle": m.get("original_title", ""),
                    "overview": m.get("overview") or "Em exibição nos cinemas.",
                    "releaseDate": m.get("release_date", ""),
                    "rating": round(float(m.get("vote_average", 0)), 1),
                    "voteCount": m.get("vote_count", 0),
                    "posterPath": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
                    "backdropPath": f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else None,
                    "popularity": m.get("popularity", 0)
                })
            output = {
                "status": "ok",
                "updatedAt": int(now),
                "releases": clean_results
            }
            if not os.path.exists(DATA_DIR):
                os.makedirs(DATA_DIR, exist_ok=True)
            with open(CINEMA_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            log_event("🎟️", "CINEMA_RELEASES", f"{len(clean_results)} filmes em cartaz atualizados via TMDb.")
            return output
    except Exception as e:
        log_event("⚠️", "CINEMA_API", f"Falha ao consultar TMDb: {e}")
        if os.path.exists(CINEMA_CACHE_FILE):
            try:
                with open(CINEMA_CACHE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"status": "error", "releases": []}

def save_user_state(state_data):
    """Persiste o progresso e favoritos globais em disco de forma atômica e thread-safe."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    with USER_STATE_LOCK:
        try:
            temp_file = USER_STATE_FILE + f".tmp.{os.getpid()}_{threading.get_ident()}"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, ensure_ascii=False, indent=2)
            os.replace(temp_file, USER_STATE_FILE)
        except Exception as e:
            print(f"Erro ao salvar user_state: {e}")

def get_vlc_path():
    """Detecta o VLC Media Player de forma dinamica e agnostica de sistema."""
    if os.path.exists(PORTABLE_VLC):
        return PORTABLE_VLC
    if os.path.exists(SYSTEM_VLC):
        return SYSTEM_VLC
    for p in [
        r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
        r"D:\Program Files\VideoLAN\VLC\vlc.exe",
        os.path.expandvars(r"%ProgramFiles%\VideoLAN\VLC\vlc.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\VideoLAN\VLC\vlc.exe"),
    ]:
        if os.path.exists(p):
            return p
    system_vlc = shutil.which("vlc")
    if system_vlc:
        return system_vlc
    if os.path.exists("/Applications/VLC.app/Contents/MacOS/VLC"):
        return "/Applications/VLC.app/Contents/MacOS/VLC"
    return None


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

CATALOG_LOCK = threading.Lock()
CACHED_CATALOG_DATA = None
_LAST_CATALOG_SCAN_TIME = 0
_CATALOG_MTIME = 0

def get_cached_catalog(force_refresh=False):
    """Carrega o catálogo compilado em cache na memória para resposta instantânea em < 2ms com proteção concorrente."""
    global CACHED_CATALOG_DATA, _LAST_CATALOG_SCAN_TIME, _CATALOG_MTIME
    catalog_json_path = os.path.join(DATA_DIR, 'catalog.json')
    now = time.time()
    
    with CATALOG_LOCK:
        # Se force_refresh foi solicitado recentemente (< 10s), reutiliza cache para prevenir DoS
        if force_refresh and (now - _LAST_CATALOG_SCAN_TIME < 10) and CACHED_CATALOG_DATA is not None:
            return CACHED_CATALOG_DATA
            
        # Se não for force_refresh e já tiver cache em memória, verifica se o arquivo em disco foi atualizado
        if not force_refresh and CACHED_CATALOG_DATA is not None:
            if os.path.exists(catalog_json_path):
                try:
                    current_mtime = os.path.getmtime(catalog_json_path)
                    if current_mtime <= _CATALOG_MTIME:
                        return CACHED_CATALOG_DATA
                except Exception:
                    return CACHED_CATALOG_DATA
            else:
                return CACHED_CATALOG_DATA

        # Tenta carregar do arquivo catalog.json compilado sem re-escanear disco
        if not force_refresh and os.path.exists(catalog_json_path):
            try:
                with open(catalog_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data and 'catalog' in data:
                        CACHED_CATALOG_DATA = data
                        _CATALOG_MTIME = os.path.getmtime(catalog_json_path)
                        return CACHED_CATALOG_DATA
            except Exception:
                pass
                
        # Compila catálogo sob demanda com lock garantindo execução única
        try:
            _LAST_CATALOG_SCAN_TIME = now
            data = build_catalog()
            CACHED_CATALOG_DATA = data
            if os.path.exists(catalog_json_path):
                _CATALOG_MTIME = os.path.getmtime(catalog_json_path)
            return data
        except Exception as e:
            log_event("⚠️", "CATÁLOGO", f"Erro ao compilar catálogo: {e}")
            if CACHED_CATALOG_DATA is not None:
                return CACHED_CATALOG_DATA
            return {"catalog": [], "movies": [], "series": []}

def extract_embedded_subtitles(video_rel):
    """Extrai legendas embutidas em formato SRT de arquivos MKV/MP4 via FFmpeg."""
    full_video_path = safe_resolve_media_path(MOVIES_DIR, video_rel)
    if not full_video_path or not os.path.exists(full_video_path):
        return {"success": False, "message": "Arquivo de vídeo não encontrado"}
    
    ffmpeg_bin = get_ffmpeg_bin()
    if not ffmpeg_bin:
        return {"success": False, "message": "FFmpeg não disponível para extração"}
    
    try:
        res = subprocess.run([ffmpeg_bin, "-i", full_video_path], capture_output=True, text=True, encoding="utf-8", errors="ignore")
        lines = res.stderr.split("\n")
        
        extracted_subs = []
        target_dir = os.path.dirname(full_video_path)
        base_name = os.path.splitext(os.path.basename(full_video_path))[0]
        
        for l in lines:
            m = re.search(r"Stream #0:(\d+)(?:\(([a-zA-Z]+)\))?.*?: Subtitle: (subrip|srt|text)", l, re.IGNORECASE)
            if m:
                stream_id = m.group(1)
                lang = (m.group(2) or "und").lower()
                is_forced = "forced" in l.lower()
                
                if lang in ("por", "pob", "pt", "bra") or lang in ("eng", "en"):
                    suffix = ".forced.srt" if is_forced else (".en.srt" if lang.startswith("en") else ".srt")
                    out_filename = f"{base_name}{suffix}"
                    out_path = os.path.join(target_dir, out_filename)
                    
                    extract_cmd = [
                        ffmpeg_bin, "-y", "-i", full_video_path,
                        "-map", f"0:{stream_id}",
                        "-c:s", "srt",
                        out_path
                    ]
                    subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
                    
                    if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
                        rel_sub_path = os.path.relpath(out_path, MOVIES_DIR).replace('\\', '/')
                        if not rel_sub_path.startswith('../'):
                            rel_sub_path = f"../{rel_sub_path}"
                        extracted_subs.append({
                            "stream": stream_id,
                            "lang": lang,
                            "filename": out_filename,
                            "path": rel_sub_path,
                            "label": ("Português (Forçada)" if is_forced else "Português (Oficial)") if lang in ("por", "pob", "pt", "bra") else "Inglês (Oficial)"
                        })
        return {
            "success": len(extracted_subs) > 0,
            "status": "ok" if len(extracted_subs) > 0 else "empty",
            "extracted": extracted_subs,
            "subtitles": extracted_subs
        }
    except Exception as e:
        return {"success": False, "message": f"Erro na extração: {e}"}

def record_watch_for_path(full_path):
    """Grava o início de reprodução no user_state para que exiba em Últimos Assistidos mesmo ao abrir no VLC."""
    try:
        catalog_data = get_cached_catalog()
        all_items = catalog_data.get('catalog', [])
        norm_target = os.path.normpath(full_path)
        
        matched_item = None
        matched_ep = None
        matched_series = None
        matched_s_idx = 0
        
        for item in all_items:
            vpath = item.get('videoPath', '')
            if vpath:
                v_res = safe_resolve_media_path(MOVIES_DIR, vpath)
                if v_res and os.path.normpath(v_res) == norm_target:
                    matched_item = item
                    break
            for s_idx, season in enumerate(item.get('seasons', [])):
                for ep in season.get('episodes', []):
                    ep_vpath = ep.get('videoPath', '')
                    if ep_vpath:
                        ep_res = safe_resolve_media_path(MOVIES_DIR, ep_vpath)
                        if ep_res and os.path.normpath(ep_res) == norm_target:
                            matched_ep = ep
                            matched_series = item
                            matched_s_idx = s_idx
                            break
                if matched_ep:
                    break
            if matched_ep:
                break
                
        state_data = load_user_state()
        wp = state_data.get('watchProgress', {})
        now_ts = int(time.time() * 1000)
        
        if matched_ep and matched_series:
            ep_id = matched_ep.get('id')
            ep_num = matched_ep.get('episodeNumber', 1)
            wp[str(ep_id)] = {
                "id": str(ep_id),
                "currentTime": 60,
                "duration": matched_ep.get('duration', 3000),
                "pct": 10,
                "completed": False,
                "timestamp": now_ts,
                "updatedAt": int(time.time()),
                "title": f"{matched_series.get('title')}: E{ep_num:02d}",
                "posterPath": matched_series.get('posterPath', ''),
                "type": 'episode',
                "isEpisode": True,
                "seriesId": matched_series.get('id'),
                "seriesTitle": matched_series.get('title'),
                "seasonIdx": matched_s_idx,
                "epNum": ep_num,
                "episodeNumber": ep_num
            }
            state_data['watchProgress'] = wp
            save_user_state(state_data)
        elif matched_item:
            m_id = matched_item.get('id')
            wp[str(m_id)] = {
                "id": str(m_id),
                "currentTime": 60,
                "duration": matched_item.get('duration', 7200),
                "pct": 10,
                "completed": False,
                "timestamp": now_ts,
                "updatedAt": int(time.time()),
                "title": matched_item.get('title', ''),
                "posterPath": matched_item.get('posterPath', ''),
                "type": 'movie',
                "isEpisode": False
            }
            state_data['watchProgress'] = wp
            save_user_state(state_data)
    except Exception as e:
        log_event("⚠️", "VLC WATCH", f"Aviso ao registrar progresso VLC: {e}")

def start_mdns_responder(ip_address, host="cinelocal"):
    """Responde a consultas mDNS na rede local para permitir acesso via http://cinelocal.local:8000/"""
    def _mdns_worker():
        MCAST_GRP = '224.0.0.251'
        MCAST_PORT = 5353
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                try:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                except Exception:
                    pass
            sock.bind(('', MCAST_PORT))
            mreq = socket.inet_aton(MCAST_GRP) + socket.inet_aton(ip_address)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except Exception:
            return

        encoded_name = b"".join([bytes([len(part)]) + part.encode('ascii') for part in [host, 'local']]) + b'\x00'
        ip_bytes = socket.inet_aton(ip_address)
        response_packet = (
            b'\x00\x00'
            b'\x84\x00'
            b'\x00\x00'
            b'\x00\x01'
            b'\x00\x00'
            b'\x00\x00'
            + encoded_name
            + b'\x00\x01'
            + b'\x80\x01'
            + b'\x00\x00\x00\x78'
            + b'\x00\x04'
            + ip_bytes
        )

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if encoded_name in data or host.encode('ascii') in data.lower():
                    sock.sendto(response_packet, (MCAST_GRP, MCAST_PORT))
            except Exception:
                time.sleep(1)

    t = threading.Thread(target=_mdns_worker, daemon=True)
    t.start()

class CineLocalStreamingHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=MOVIES_DIR, **kwargs)

    def log_message(self, format, *args):
        # Silencia o spam das requisições HTTP 200/206/304 rotineiras
        pass

    def log_error(self, format, *args):
        # Ignora ruídos comuns de desconexão rápida durante seek de vídeo
        msg = format % args
        if any(err in msg for err in ['10054', '10053', 'Broken pipe', 'ConnectionResetError']):
            return
        log_event("⚠️", "AVISO", msg)

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def end_headers(self):
        clean_path = self.path.split('?')[0].lower()
        if clean_path.endswith(('.html', '.js', '.json')) or clean_path in ('/', '/app', '/app/'):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        client_ip = self.client_address[0]
        parsed = urllib.parse.urlparse(self.path)
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            payload = json.loads(body.decode('utf-8')) if body else {}
        except Exception:
            payload = {}

        # 1. Comando do Controle Remoto Virtual
        if parsed.path == '/api/remote/action':
            action = payload.get('action') or urllib.parse.parse_qs(parsed.query).get('action', [''])[0]
            if action:
                ev = REMOTE_HUB.dispatch(action, payload)
                if should_log_activity(('remote', client_ip, action), 2):
                    log_event("📱", "REMOTE ACTION", f"Comando '{action}' recebido de {client_ip}")
                res = json.dumps({"status": "ok", "action": action, "id": ev["id"]}).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(res)
                return
            self.send_error(400, 'Ação não informada')
            return

        # 2. Sincronização de Progresso de Reprodução (Continuar Assistindo)
        if parsed.path == '/api/progress':
            media_id = payload.get('id')
            current_time = float(payload.get('currentTime', 0))
            duration = float(payload.get('duration', 0))
            item_info = payload.get('item', {})
            
            if media_id:
                state_data = load_user_state()
                wp = state_data.get('watchProgress', {})
                wl = state_data.get('watchedList', {})
                
                # Se duration for 0 ou desconhecida, estima com base no tipo
                if duration <= 0:
                    duration = 3000.0 if item_info.get('isEpisode') else 7200.0
                
                pct = int(round((current_time / duration) * 100)) if duration > 0 else int(payload.get('pct', 0))
                pct = max(0, min(100, pct))
                completed = bool(duration > 0 and (pct >= 90 or (current_time / duration) > 0.90 or payload.get('completed')))
                now_ts = int(time.time() * 1000)
                
                ep_num = item_info.get('epNum', item_info.get('episodeNumber', None))
                
                wp[str(media_id)] = {
                    "id": str(media_id),
                    "currentTime": current_time,
                    "duration": duration,
                    "pct": pct,
                    "completed": completed,
                    "timestamp": now_ts,
                    "updatedAt": int(time.time()),
                    "title": item_info.get('title', ''),
                    "posterPath": item_info.get('posterPath', ''),
                    "type": 'episode' if item_info.get('isEpisode') else 'movie',
                    "isEpisode": item_info.get('isEpisode', False),
                    "seriesId": item_info.get('seriesId', None),
                    "seriesTitle": item_info.get('seriesTitle', None),
                    "seasonIdx": item_info.get('seasonIdx', None),
                    "epNum": ep_num,
                    "episodeNumber": ep_num
                }
                if completed:
                    wl[str(media_id)] = True
                    
                state_data['watchProgress'] = wp
                state_data['watchedList'] = wl
                save_user_state(state_data)
                
                res = json.dumps({"status": "ok", "id": media_id, "pct": pct, "completed": completed}).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(res)
                return
            self.send_error(400, 'ID não informado')
            return

        # 2.1 Alternar Status de Assistido (Já Assistidos)
        if parsed.path == '/api/watched/toggle':
            media_id = str(payload.get('id', ''))
            if media_id:
                state_data = load_user_state()
                wl = state_data.get('watchedList', {})
                wp = state_data.get('watchProgress', {})
                is_watched = not bool(wl.get(media_id))
                if is_watched:
                    wl[media_id] = True
                    if media_id in wp:
                        wp[media_id]['completed'] = True
                        wp[media_id]['pct'] = 100
                else:
                    if media_id in wl:
                        del wl[media_id]
                    if media_id in wp:
                        wp[media_id]['completed'] = False
                state_data['watchedList'] = wl
                state_data['watchProgress'] = wp
                save_user_state(state_data)
                res = json.dumps({"status": "ok", "id": media_id, "watched": is_watched}).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(res)
                return
            self.send_error(400, 'ID não informado')
            return

        # 3. Alternar Favorito (Minha Lista)
        if parsed.path == '/api/favorite/toggle':
            media_id = str(payload.get('id', ''))
            if media_id:
                state_data = load_user_state()
                favs = state_data.get('favorites', [])
                if media_id in favs:
                    favs.remove(media_id)
                    is_fav = False
                else:
                    favs.append(media_id)
                    is_fav = True
                state_data['favorites'] = favs
                save_user_state(state_data)
                
                res = json.dumps({"status": "ok", "id": media_id, "isFavorite": is_fav, "favorites": favs}).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(res)
                return
            self.send_error(400, 'ID não informado')
            return

        self.send_error(404, 'Rota POST não encontrada')

    def do_GET(self):
        client_ip = self.client_address[0]
        parsed = urllib.parse.urlparse(self.path)

        # Suporte a PWA Manifest e Service Worker
        if parsed.path == '/manifest.json':
            manifest_file = os.path.join(APP_DIR, 'manifest.json')
            if os.path.exists(manifest_file):
                with open(manifest_file, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/manifest+json; charset=utf-8')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
                return

        if parsed.path == '/sw.js':
            sw_file = os.path.join(APP_DIR, 'sw.js')
            if os.path.exists(sw_file):
                with open(sw_file, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/javascript; charset=utf-8')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Service-Worker-Allowed', '/')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
                return

        if parsed.path in ('/icon-192.png', '/icon-512.png'):
            icon_file = os.path.join(APP_DIR, os.path.basename(parsed.path))
            if os.path.exists(icon_file):
                with open(icon_file, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
                return

        # Atalho para o Controle Remoto Virtual
        if parsed.path in ('/remote', '/remote/', '/controle', '/controle/'):
            self.send_response(302)
            self.send_header('Location', '/app/remote.html')
            self.end_headers()
            return

        # API SSE para o Controle Remoto na TV/PC
        if parsed.path == '/api/remote/events':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            q = REMOTE_HUB.subscribe()
            try:
                self.wfile.write(b": connected\n\n")
                self.wfile.flush()
                while True:
                    try:
                        ev = q.get(timeout=25)
                        msg = f"data: {json.dumps(ev)}\n\n".encode('utf-8')
                        self.wfile.write(msg)
                        self.wfile.flush()
                    except queue.Empty:
                        self.wfile.write(b": ping\n\n")
                        self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                REMOTE_HUB.unsubscribe(q)
            return

        # Fallback polling para o Controle Remoto
        if parsed.path == '/api/remote/poll':
            query_params = urllib.parse.parse_qs(parsed.query)
            since_id = int(query_params.get('since', ['0'])[0])
            events = REMOTE_HUB.get_events_since(since_id)
            data = json.dumps({"events": events}, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
            return

        # Estado global do usuário (Progresso, Favoritos e Assistidos)
        if parsed.path == '/api/user_state':
            state_data = load_user_state()
            data = json.dumps(state_data, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
            return

        # Filmes em Cartaz nos Cinemas (TMDb Now Playing)
        if parsed.path == '/api/cinema_releases':
            releases_data = get_cinema_releases()
            data = json.dumps(releases_data, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
            return

        # Detecção de faixas de áudio do arquivo
        if parsed.path == '/api/audio_info':
            query_params = urllib.parse.parse_qs(parsed.query)
            video_rel = query_params.get('path', [''])[0]
            full_movie_path = safe_resolve_media_path(MOVIES_DIR, video_rel)
            if not full_movie_path or not os.path.exists(full_movie_path):
                self.send_error(404, 'Arquivo de vídeo não encontrado ou caminho inválido')
                return
            info_data = get_audio_streams_info(full_movie_path)
            data = json.dumps(info_data, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
            return

        # Busca e download automático de legendas online
        if parsed.path == '/api/buscar_legendas':
            query_params = urllib.parse.parse_qs(parsed.query)
            video_rel = query_params.get('path', query_params.get('video', ['']))[0]
            title = query_params.get('title', [''])[0]
            imdb = query_params.get('imdb', query_params.get('imdb_id', query_params.get('imdbUrl', [''])))[0]
            season = query_params.get('season', [None])[0]
            episode = query_params.get('episode', [None])[0]
            
            if not video_rel or not safe_resolve_media_path(MOVIES_DIR, video_rel):
                res_data = {"success": False, "status": "error", "message": "Caminho de vídeo inválido ou não fornecido"}
                data = json.dumps(res_data, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
                return
            
            res_data = download_online_subtitle(
                video_rel=video_rel,
                query_title=title,
                imdb_id=imdb,
                season=season,
                episode=episode
            )
            data = json.dumps(res_data, ensure_ascii=False).encode('utf-8')
            status_code = 200 if res_data.get('success') else 404
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
            return
        
        # Redireciona a raiz para a aplicação CineLocal
        if parsed.path in ('/', '', '/index.html'):
            if should_log_activity(('ui', client_ip), 10):
                log_event("🌐", "INTERFACE", f"Cliente conectado ({client_ip})")
            self.send_response(302)
            self.send_header('Location', '/app/index.html')
            self.end_headers()
            return

        # Suporte a arquivos estáticos do PWA na raiz
        if parsed.path in ('/manifest.json', '/sw.js', '/icon-192.png', '/icon-512.png'):
            target_f = os.path.join(APP_DIR, parsed.path.lstrip('/'))
            if os.path.exists(target_f):
                content_type = 'application/manifest+json' if parsed.path.endswith('.json') else ('application/javascript' if parsed.path.endswith('.js') else 'image/png')
                with open(target_f, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.end_headers()
                self.wfile.write(data)
                return
            
        if parsed.path in ('/app/index.html', '/app/'):
            if should_log_activity(('ui', client_ip), 10):
                log_event("🌐", "INTERFACE", f"Cliente conectado ({client_ip})")

        if parsed.path.startswith('/CineLocal/'):
            self.send_response(301)
            self.send_header('Location', parsed.path.replace('/CineLocal/', '/app/'))
            self.end_headers()
            return
            
        # API de recursos do ambiente (VLC e FFmpeg disponíveis)
        if parsed.path in ('/api/capabilities', '/api/status'):
            vlc_bin = get_vlc_path()
            ffmpeg_bin = get_ffmpeg_bin()
            local_ip = get_local_ip()
            hostname = socket.gethostname().lower()
            data = json.dumps({
                "vlcAvailable": bool(vlc_bin),
                "vlcPath": vlc_bin or "",
                "ffmpegAvailable": bool(ffmpeg_bin),
                "ffmpegPath": ffmpeg_bin or "",
                "localIp": local_ip,
                "localUrl": f"http://{local_ip}:{PORT}/",
                "genericUrl": f"http://cinelocal.local:{PORT}/",
                "hostname": hostname,
                "hostnameUrl": f"http://{hostname}.local:{PORT}/"
            }, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
            return

        # API para extrair legendas embutidas em MKV/MP4
        if parsed.path == '/api/extract_subtitles':
            try:
                query_params = urllib.parse.parse_qs(parsed.query)
                video_rel = query_params.get('path', [''])[0]
                if not video_rel or not safe_resolve_media_path(MOVIES_DIR, video_rel):
                    res = {"success": False, "message": "Caminho de vídeo inválido ou não fornecido"}
                else:
                    res = extract_embedded_subtitles(video_rel)
                data = json.dumps(res, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
                return
            except Exception as e:
                self.send_error(500, f'Erro na extração de legendas: {e}')
                return

        # API para sincronizar catálogo dinamicamente (Cache em memória instantâneo)
        if parsed.path == '/api/filmes':
            try:
                query_params = urllib.parse.parse_qs(parsed.query)
                force_refresh = query_params.get('refresh', ['0'])[0] in ('1', 'true', 'True')
                if force_refresh and should_log_activity(('catalog_refresh', client_ip), 5):
                    log_event("⚡", "CATÁLOGO", f"Recompilação de catálogo solicitada por {client_ip}")
                catalog = get_cached_catalog(force_refresh=force_refresh)
                data = json.dumps(catalog, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
                return
            except Exception as e:
                log_event("❌", "ERRO", f"Falha ao carregar catálogo: {e}")
                self.send_error(500, f'Erro ao carregar catálogo: {e}')
                return

        # API para abrir filme diretamente no VLC instalado no PC
        if parsed.path == '/api/open_vlc':
            try:
                query_params = urllib.parse.parse_qs(parsed.query)
                video_rel = query_params.get('path', [''])[0]
                full_movie_path = safe_resolve_media_path(MOVIES_DIR, video_rel) if video_rel else None
                if full_movie_path:
                    vlc_bin = get_vlc_path()
                    if os.path.exists(full_movie_path) and vlc_bin and os.path.exists(vlc_bin):
                        # Registra reprodução no histórico e últimos assistidos
                        record_watch_for_path(full_movie_path)
                        creation_flag = (subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000008) if sys.platform == 'win32' else 0
                        vlc_cmd = [vlc_bin, full_movie_path]
                        
                        # Se houver legenda .srt externa correspondente, passa automaticamente para o VLC
                        base_no_ext = os.path.splitext(full_movie_path)[0]
                        candidate_srt = base_no_ext + '.srt'
                        if os.path.exists(candidate_srt):
                            vlc_cmd.extend(['--sub-file', candidate_srt])
                            
                        subprocess.Popen(
                            vlc_cmd,
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            close_fds=True,
                            creationflags=creation_flag
                        )
                        movie_name = os.path.basename(full_movie_path)
                        log_event("🚀", "VLC EXTERNO", f"Abrindo '{movie_name}' ({client_ip})")
                        response_data = json.dumps({"status": "ok", "message": "VLC iniciado", "vlc": vlc_bin}).encode('utf-8')
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json; charset=utf-8')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(response_data)
                        return
                    else:
                        response_data = json.dumps({"status": "error", "message": "Arquivo ou VLC não encontrado"}).encode('utf-8')
                        self.send_response(404)
                        self.send_header('Content-Type', 'application/json; charset=utf-8')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(response_data)
                        return
                else:
                    response_data = json.dumps({"status": "error", "message": "Caminho de vídeo inválido ou não fornecido"}).encode('utf-8')
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(response_data)
                    return
            except Exception as e:
                self.send_error(500, f'Erro ao abrir no VLC: {e}')
        # API de streaming em tempo real com áudio compatível para navegador/TV
        if parsed.path == '/api/stream':
            try:
                query_params = urllib.parse.parse_qs(parsed.query)
                video_rel = query_params.get('path', [''])[0]
                ss = query_params.get('ss', ['0'])[0]
                audio_idx = query_params.get('audio', [''])[0]
                
                full_movie_path = safe_resolve_media_path(MOVIES_DIR, video_rel)
                ffmpeg_bin = get_ffmpeg_bin()
                if not full_movie_path or not os.path.exists(full_movie_path) or not ffmpeg_bin:
                    self.send_error(404, 'Arquivo ou FFmpeg não encontrado')
                    return
                
                if not audio_idx:
                    audio_idx = get_best_audio_stream(full_movie_path)
                
                movie_name = os.path.basename(full_movie_path)
                log_event("🔊", "DIRECT STREAM", f"Transcodificando áudio AAC para '{movie_name}' ({client_ip})")

                # Monta comando FFmpeg Direct Stream (Vídeo cópia 100%, Áudio AAC estéreo)
                cmd = [
                    ffmpeg_bin,
                    "-nostdin",
                    "-nostats",
                    "-loglevel", "error",
                    "-ss", str(ss),
                    "-i", full_movie_path,
                    "-map", "0:v:0",
                    "-map", f"0:{audio_idx}",
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-ac", "2",
                    "-f", "mp4",
                    "-movflags", "frag_keyframe+empty_moov+default_base_moof",
                    "pipe:1"
                ]
                
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
                
                self.send_response(200)
                self.send_header('Content-Type', 'video/mp4')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                
                try:
                    while True:
                        chunk = proc.stdout.read(65536)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                finally:
                    proc.kill()
                    try:
                        proc.wait(timeout=1)
                    except Exception:
                        pass
                return
            except Exception as e:
                self.send_error(500, f'Erro no streaming: {e}')
                return
        
        return super().do_GET()

    def send_head(self):
        """Suporte a HTTP 206 Partial Content / Range para seek rápido em vídeos"""
        path = self.translate_path(self.path)
        real_base = os.path.realpath(MOVIES_DIR)
        real_target = os.path.realpath(path)
        if not (real_target == real_base or real_target.startswith(real_base + os.sep)):
            self.send_error(403, 'Acesso proibido')
            return None

        if os.path.isdir(path):
            return super().send_head()
            
        if not os.path.exists(path):
            self.send_error(404, 'Arquivo não encontrado')
            return None
        
        lower_path = path.lower()
        client_ip = self.client_address[0]
        if any(lower_path.endswith(ext) for ext in ('.mp4', '.mkv', '.avi', '.mov', '.webm')):
            fname = os.path.basename(path)
            if should_log_activity(('stream', client_ip, path), 12):
                log_event("🍿", "STREAMING", f"Reproduzindo '{fname}' para {client_ip}")
        elif lower_path.endswith('.srt'):
            fname = os.path.basename(path)
            if should_log_activity(('sub', client_ip, path), 10):
                log_event("💬", "LEGENDA", f"Carregando legenda: '{fname}' ({client_ip})")

        ctype = self.guess_type(path)
        if lower_path.endswith('.mkv'):
            ctype = 'video/x-matroska'
        elif lower_path.endswith('.mp4'):
            ctype = 'video/mp4'
        elif lower_path.endswith('.srt'):
            ctype = 'text/plain; charset=utf-8'

        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, 'Erro ao abrir arquivo')
            return None

        fs = os.fstat(f.fileno())
        size = fs[6]
        
        range_header = self.headers.get('Range')
        if range_header and range_header.startswith('bytes='):
            try:
                parts = range_header.split('=')[1].strip().split('-')
                start = int(parts[0]) if parts[0] else 0
                end = int(parts[1]) if parts[1] else size - 1
                if start >= size:
                    self.send_error(416, 'Requested range not satisfiable')
                    f.close()
                    return None
                end = min(end, size - 1)
                length = end - start + 1
                
                self.send_response(206)
                self.send_header('Content-Type', ctype)
                self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
                self.send_header('Content-Length', str(length))
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                f.seek(start)
                return f
            except Exception:
                pass
        
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(size))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        return f

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def is_port_in_use(port):
    """Verifica se o servidor CineLocal já está em execução nesta porta."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

def run():
    open_browser = True
    if '--no-browser' in sys.argv:
        open_browser = False
    elif '--browser' in sys.argv:
        open_browser = True

    local_ip = get_local_ip()
    hostname = socket.gethostname().lower()
    local_url = f'http://localhost:{PORT}/'
    tv_url = f'http://{local_ip}:{PORT}/'
    generic_url = f'http://cinelocal.local:{PORT}/'
    hostname_url = f'http://{hostname}.local:{PORT}/'

    # Se o servidor já estiver rodando, não duplica nem trava com erro de socket
    if is_port_in_use(PORT):
        print("\n" + "=" * 76)
        print(f"  🍿 CINELOCAL • O SERVIDOR JÁ ESTÁ EM EXECUÇÃO NA PORTA {PORT}")
        print("=" * 76)
        print(f"\n  🌐 No seu Computador:   {local_url}")
        print(f"  📺 Endereço Genérico:   {generic_url}")
        print(f"  📱 Na sua Smart TV:     {tv_url}\n")
        if open_browser:
            print("  🚀 Abrindo o CineLocal no navegador...\n")
            try:
                webbrowser.open(local_url)
            except Exception:
                pass
        return

    # Inicia o responder mDNS em segundo plano para que cinelocal.local funcione na rede Wi-Fi
    try:
        start_mdns_responder(local_ip, host="cinelocal")
    except Exception:
        pass

    # Sincroniza o catálogo apenas se catalogo.js ou data/catalog.json ainda não existirem
    catalog_path = os.path.join(APP_DIR, 'catalogo.js')
    catalog_json = os.path.join(DATA_DIR, 'catalog.json')
    if not os.path.exists(catalog_path) or not os.path.exists(catalog_json):
        print("\n📦 Primeiro uso detectado: gerando catálogo inicial...")
        try:
            get_cached_catalog(force_refresh=True)
        except Exception as e:
            log_event("⚠️", "CATÁLOGO", f"Aviso ao compilar catálogo: {e}")
    else:
        # Carrega o catálogo na memória em < 2ms
        get_cached_catalog(force_refresh=False)
    
    vlc_bin = get_vlc_path()
    ffmpeg_bin = get_ffmpeg_bin()
    vlc_status = f"✅ Ativo ({os.path.basename(vlc_bin)})" if vlc_bin else "⚠️  Não detectado (Opcional - codecs TrueHD/DTS)"
    ffmpeg_status = f"✅ Ativo ({os.path.basename(ffmpeg_bin)})" if ffmpeg_bin else "⚠️  Não detectado (Opcional - áudio web)"

    banner = f"""
================================================================================
  🍿 CINELOCAL • SERVIDOR DE STREAMING ATIVO (MULTITHREAD)
================================================================================

  🌐 No seu Computador:   {local_url}
  📺 Endereço Genérico:   {generic_url}
  📱 Na Smart TV / Cel:   {tv_url} ou {hostname_url}
  🎮 Controle Remoto:     {generic_url}remote

  ⚡ HTTP 206 Streaming:  Ativo (seek instantâneo em 1080p e 4K)
  🚀 VLC Media Player:    {vlc_status}
  🎵 Motor FFmpeg:        {ffmpeg_status}

  💡 Pressione Ctrl + C no terminal para encerrar o servidor.
================================================================================
"""
    print(banner)
    print("📡 Aguardando conexões e reproduções de mídia...\n")
    
    if open_browser:
        def _open_single_tab():
            time.sleep(0.4)
            try:
                webbrowser.open(local_url)
            except Exception:
                pass
        threading.Thread(target=_open_single_tab, daemon=True).start()
    
    with ThreadingServer(('0.0.0.0', PORT), CineLocalStreamingHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Servidor CineLocal encerrado com sucesso. Bom filme!\n")

if __name__ == '__main__':
    run()

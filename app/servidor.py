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

from atualizar_catalogo import build_catalog

PORTABLE_VLC = os.path.join(APP_DIR, "vlc", "vlc.exe")
SYSTEM_VLC = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

AUDIO_CACHE = {}
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
    """Detecta as faixas de áudio disponíveis no vídeo via FFmpeg."""
    ffmpeg_bin = get_ffmpeg_bin()
    if not ffmpeg_bin or not os.path.exists(movie_path):
        return []
    try:
        res = subprocess.run(
            [ffmpeg_bin, "-i", movie_path],
            capture_output=True, text=True, encoding="utf-8", errors="ignore"
        )
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
        return streams
    except Exception as e:
        print(f"Erro ao extrair audio_info: {e}")
        return []

DATA_DIR = os.path.join(APP_DIR, "data")
USER_STATE_FILE = os.path.join(DATA_DIR, "user_state.json")

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

def load_user_state():
    """Carrega o progresso e favoritos globais sincronizados entre dispositivos."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(USER_STATE_FILE):
        try:
            with open(USER_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"watchProgress": {}, "favorites": []}

def save_user_state(state_data):
    """Persiste o progresso e favoritos globais em disco."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(USER_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state_data, f, ensure_ascii=False, indent=2)
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
                completed = bool(duration > 0 and (current_time / duration) > 0.92)
                
                wp[str(media_id)] = {
                    "currentTime": current_time,
                    "duration": duration,
                    "completed": completed,
                    "updatedAt": int(time.time()),
                    "title": item_info.get('title', ''),
                    "posterPath": item_info.get('posterPath', ''),
                    "isEpisode": item_info.get('isEpisode', False),
                    "seriesId": item_info.get('seriesId', None),
                    "seasonIdx": item_info.get('seasonIdx', None),
                    "episodeNumber": item_info.get('episodeNumber', None)
                }
                state_data['watchProgress'] = wp
                save_user_state(state_data)
                
                res = json.dumps({"status": "ok", "id": media_id, "completed": completed}).encode('utf-8')
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

        # Estado global do usuário (Progresso e Favoritos)
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

        # Detecção de faixas de áudio do arquivo
        if parsed.path == '/api/audio_info':
            query_params = urllib.parse.parse_qs(parsed.query)
            video_rel = query_params.get('path', [''])[0]
            clean_rel = urllib.parse.unquote(video_rel).replace('../', '').lstrip('/').replace('/', os.sep)
            full_movie_path = os.path.join(MOVIES_DIR, clean_rel)
            streams = get_audio_streams_info(full_movie_path)
            data = json.dumps({"streams": streams}, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
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
            data = json.dumps({
                "vlcAvailable": bool(vlc_bin),
                "vlcPath": vlc_bin or "",
                "ffmpegAvailable": bool(ffmpeg_bin),
                "ffmpegPath": ffmpeg_bin or "",
                "localIp": local_ip,
                "localUrl": f"http://{local_ip}:{PORT}/"
            }, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
            return

        # API para sincronizar catálogo dinamicamente
        if parsed.path == '/api/filmes':
            try:
                if should_log_activity(('catalog', client_ip), 5):
                    log_event("⚡", "CATÁLOGO", f"Sincronização solicitada por {client_ip}")
                catalog = build_catalog()
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
                if video_rel:
                    clean_rel = urllib.parse.unquote(video_rel).replace('../', '').lstrip('/').replace('/', os.sep)
                    full_movie_path = os.path.join(MOVIES_DIR, clean_rel)
                    
                    vlc_bin = get_vlc_path()
                    if os.path.exists(full_movie_path) and vlc_bin and os.path.exists(vlc_bin):
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
            except Exception as e:
                self.send_error(500, f'Erro ao abrir no VLC: {e}')
        # API de streaming em tempo real com áudio compatível para navegador/TV
        if parsed.path == '/api/stream':
            try:
                query_params = urllib.parse.parse_qs(parsed.query)
                video_rel = query_params.get('path', [''])[0]
                ss = query_params.get('ss', ['0'])[0]
                audio_idx = query_params.get('audio', [''])[0]
                
                clean_rel = urllib.parse.unquote(video_rel).replace('../', '').lstrip('/').replace('/', os.sep)
                full_movie_path = os.path.join(MOVIES_DIR, clean_rel)
                
                ffmpeg_bin = get_ffmpeg_bin()
                if not os.path.exists(full_movie_path) or not ffmpeg_bin:
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
    local_url = f'http://localhost:{PORT}/'
    tv_url = f'http://{local_ip}:{PORT}/'

    # Se o servidor já estiver rodando, não duplica nem trava com erro de socket
    if is_port_in_use(PORT):
        print("\n" + "=" * 76)
        print(f"  🍿 CINELOCAL • O SERVIDOR JÁ ESTÁ EM EXECUÇÃO NA PORTA {PORT}")
        print("=" * 76)
        print(f"\n  🌐 No seu Computador:   {local_url}")
        print(f"  📺 Na sua Smart TV:     {tv_url}\n")
        if open_browser:
            print("  🚀 Abrindo o CineLocal no navegador...\n")
            try:
                webbrowser.open(local_url)
            except Exception:
                pass
        return

    # Sincroniza o catálogo apenas se catalogo.js ainda não existir (primeira vez)
    catalog_path = os.path.join(APP_DIR, 'catalogo.js')
    if not os.path.exists(catalog_path):
        print("\n📦 Primeiro uso detectado: gerando catálogo inicial...")
        try:
            build_catalog()
        except Exception as e:
            log_event("⚠️", "CATÁLOGO", f"Aviso ao compilar catálogo: {e}")
    
    vlc_bin = get_vlc_path()
    ffmpeg_bin = get_ffmpeg_bin()
    vlc_status = f"✅ Ativo ({os.path.basename(vlc_bin)})" if vlc_bin else "⚠️  Não detectado (Opcional - codecs TrueHD/DTS)"
    ffmpeg_status = f"✅ Ativo ({os.path.basename(ffmpeg_bin)})" if ffmpeg_bin else "⚠️  Não detectado (Opcional - áudio web)"

    banner = f"""
================================================================================
  🍿 CINELOCAL • SERVIDOR DE STREAMING ATIVO (MULTITHREAD)
================================================================================

  🌐 No seu Computador:   {local_url}
  📺 Na sua Smart TV:     {tv_url}
  📱 No Celular / Tablet: {tv_url}
  🎮 Controle Remoto:     {tv_url}remote

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

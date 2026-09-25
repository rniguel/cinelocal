# -*- coding: utf-8 -*-
"""
Script de atualização do catálogo e legendas para o CineLocal.
Escaneia as pastas media/filmes e media/series, extrai metadados e compila o catalogo.js.
Higieniza tags de legendas (eliminando tags indesejadas como <font>, {y:i}, etc.).
"""

import os
import json
import re
import subprocess
import sys
import shutil

# Ensure APP_DIR is in sys.path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from metadata_db import get_movie_info, get_series_info
ROOT_DIR = os.path.dirname(APP_DIR)
MEDIA_DIR = os.path.join(ROOT_DIR, 'media')
FILMES_DIR = os.path.join(MEDIA_DIR, 'filmes')
SERIES_DIR = os.path.join(MEDIA_DIR, 'series')
AUDIO_CACHE_FILE = os.path.join(APP_DIR, '.audio_cache.json')

def get_ffmpeg_bin():
    """Localiza o FFmpeg na pasta app/bin, no PATH do sistema ou em caminhos padroes."""
    local_bin = os.path.join(APP_DIR, 'bin', 'ffmpeg.exe')
    if os.path.exists(local_bin):
        return local_bin
    system_bin = shutil.which('ffmpeg')
    if system_bin:
        return system_bin
    for candidate in [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe')
    ]:
        if os.path.exists(candidate):
            return candidate
    return None

def load_audio_cache():
    if os.path.exists(AUDIO_CACHE_FILE):
        try:
            with open(AUDIO_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_audio_cache(cache):
    try:
        with open(AUDIO_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def probe_audio_and_subs(filepath, cache):
    try:
        mtime = os.path.getmtime(filepath)
    except Exception:
        return {'audio': 'DUB', 'audioLabel': 'Dublado', 'hasEmbeddedSubtitles': False}
    
    norm_path = os.path.normpath(filepath)
    if norm_path in cache and cache[norm_path].get('mtime') == mtime:
        return cache[norm_path]
    
    audio_langs = []
    has_sub = False
    lower_name = os.path.basename(filepath).lower()
    
    ffmpeg_bin = get_ffmpeg_bin()
    if ffmpeg_bin:
        try:
            cmd = [ffmpeg_bin, '-i', filepath]
            proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, encoding='utf-8', errors='ignore')
            for line in proc.stderr.splitlines():
                if 'Audio:' in line:
                    m = re.search(r'Stream #0:\d+(?:\[0x[0-9a-fA-F]+\])?(?:\(([a-zA-Z]{2,4})\))?: Audio:', line)
                    lang = m.group(1).lower() if (m and m.group(1)) else 'und'
                    audio_langs.append(lang)
                if 'Subtitle:' in line:
                    has_sub = True
        except Exception:
            pass
            
    has_por = any(l in ('por', 'pob', 'pt', 'bra', 'portuguese') for l in audio_langs)
    has_other = any(l in ('eng', 'und', 'jpn', 'fre', 'spa', 'ger', 'ita', 'english') for l in audio_langs)
    
    if 'dual' in lower_name or (has_por and has_other) or len(audio_langs) > 1:
        audio_type = 'DUAL'
        audio_label = 'Dual Áudio'
    elif has_por or 'dub' in lower_name:
        audio_type = 'DUB'
        audio_label = 'Dublado'
    elif has_other or 'leg' in lower_name:
        audio_type = 'LEG'
        audio_label = 'Legendado'
    else:
        audio_type = 'DUB'
        audio_label = 'Dublado'
        
    info = {
        'mtime': mtime,
        'audio': audio_type,
        'audioLabel': audio_label,
        'audioTracks': audio_langs,
        'hasEmbeddedSubtitles': has_sub
    }
    cache[norm_path] = info
    return info


def clean_sub_text(raw_text):
    if not raw_text:
        return ''
    # Remove tags de posicionamento ASS/SSA como {\an8}, {y:i}, etc.
    t = re.sub(r'\{[^}]+\}', '', raw_text)
    # Remove tags <font ...> e </font>
    t = re.sub(r'</?font[^>]*>', '', t, flags=re.IGNORECASE)
    # Converte <br/> para \n para padronizar
    t = re.sub(r'<br\s*/?>', '\n', t, flags=re.IGNORECASE)
    # Limpa tags HTML residuais
    t = re.sub(r'</?(?!i|b|u\b)[a-z0-9_-]+[^>]*>', '', t, flags=re.IGNORECASE)
    return t.strip()

def parse_srt(content):
    blocks = re.split(r'\r?\n\r?\n+', content.strip())
    cues = []
    for b in blocks:
        lines = b.strip().split('\n')
        if len(lines) < 2:
            continue
        idx = 1 if lines[0].strip().isdigit() else 0
        if idx >= len(lines) or '-->' not in lines[idx]:
            continue
        m = re.match(r'(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})', lines[idx])
        if not m:
            continue
        s = int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3)) + int(m.group(4))/1000.0
        e = int(m.group(5))*3600 + int(m.group(6))*60 + int(m.group(7)) + int(m.group(8))/1000.0
        raw_txt = '\n'.join(lines[idx+1:]).strip()
        cleaned_txt = clean_sub_text(raw_txt)
        if cleaned_txt:
            cues.append([round(s, 2), round(e, 2), cleaned_txt])
    return cues

def get_resolution(name):
    if '2160p' in name or '4K' in name:
        return '4K UHD'
    elif '1080p' in name:
        return '1080p'
    elif '720p' in name:
        return '720p'
    return 'HD'

def get_year(name):
    m = re.search(r'\((\d{4})\)', name)
    return int(m.group(1)) if m else 0

def clean_title(name):
    stem = os.path.splitext(name)[0]
    stem = re.sub(r'\s*\[.*?\]', '', stem)
    stem = re.sub(r'\s*\(\d{4}\)', '', stem)
    stem = re.sub(r'^\d{2}\s*-\s*', '', stem)
    return stem.strip()

def parse_subtitles_for_dir(dir_path, rel_prefix, subtitles_db):
    srts = [f for f in sorted(os.listdir(dir_path)) if f.lower().endswith('.srt')]
    subtitles = []
    for s in srts:
        srel = f'{rel_prefix}/{s}'.replace('\\', '/')
        label = 'Português'
        if '.forced' in s.lower():
            label = 'Português (Forçada)'
        elif '.en' in s.lower():
            label = 'Inglês'
        elif '.pt' in s.lower():
            label = 'Português (Brasil)'
        
        subtitles.append({
            'filename': s,
            'path': srel,
            'label': label
        })
        content = None
        for enc in ('utf-8-sig', 'utf-8', 'cp1252', 'latin-1'):
            try:
                with open(os.path.join(dir_path, s), 'r', encoding=enc) as sf:
                    content = sf.read()
                    break
            except Exception:
                continue
        if content:
            subtitles_db[srel] = parse_srt(content)
        else:
            print(f'Erro ao ler legenda {srel}')
    return subtitles

def build_catalog():
    movies_catalog = []
    series_catalog = []
    subtitles_db = {}
    audio_cache = load_audio_cache()
    
    # Garante que as pastas de mídia existam
    os.makedirs(FILMES_DIR, exist_ok=True)
    os.makedirs(SERIES_DIR, exist_ok=True)
    
    # Aviso informativo caso o FFmpeg não esteja presente
    if not get_ffmpeg_bin():
        print('[INFO] FFmpeg não encontrado (opcional). A detecção de áudio usará padrões rápidos.')
        print('       Para suporte completo a codecs de áudio avançados, instale o FFmpeg: https://ffmpeg.org/download.html\n')
    
    # -------------------------------------------------------------
    # 1. PROCESSAR FILMES (media/filmes)
    # -------------------------------------------------------------
    if os.path.exists(FILMES_DIR):
        for item in sorted(os.listdir(FILMES_DIR)):
            ipath = os.path.join(FILMES_DIR, item)
            if not os.path.isdir(ipath) or item.startswith('.'):
                continue
            
            subdirs = [d for d in sorted(os.listdir(ipath)) if os.path.isdir(os.path.join(ipath, d))]
            
            if subdirs:
                # Franquia / Coleção com subpastas numeradas (Marvel, Star Wars, Batman, etc.)
                franchise_name = item
                for sd in subdirs:
                    sd_path = os.path.join(ipath, sd)
                    files = sorted(os.listdir(sd_path))
                    videos = [f for f in files if f.lower().endswith(('.mkv', '.mp4'))]
                    posters = [f for f in files if f.lower() == 'poster.jpg']
                    
                    seq_match = re.match(r'^(\d{2})\s*-\s*(.*)', sd)
                    seq_num = int(seq_match.group(1)) if seq_match else None
                    
                    rel_prefix = f'../media/filmes/{item}/{sd}'
                    v_subtitles = parse_subtitles_for_dir(sd_path, rel_prefix, subtitles_db)
                    
                    for v in videos:
                        vrel = f'{rel_prefix}/{v}'.replace('\\', '/')
                        prel = f'{rel_prefix}/poster.jpg'.replace('\\', '/') if posters else ''
                        full_vpath = os.path.join(sd_path, v)
                        v_size = os.path.getsize(full_vpath)
                        v_audio = probe_audio_and_subs(full_vpath, audio_cache)
                        has_subs = bool(len(v_subtitles) > 0 or v_audio.get('hasEmbeddedSubtitles'))
                        m_title = clean_title(v) or clean_title(sd)
                        m_year = get_year(v) or get_year(sd)
                        m_meta = get_movie_info(m_title, year=m_year, franchise=franchise_name)
                        
                        movies_catalog.append({
                            'id': f'mov_{len(movies_catalog)+1}',
                            'type': 'movie',
                            'title': m_title,
                            'rawName': v,
                            'franchise': franchise_name,
                            'sequence': seq_num,
                            'folder': sd,
                            'year': m_year,
                            'resolution': get_resolution(v),
                            'format': os.path.splitext(v)[1][1:].upper(),
                            'isExtended': 'Versão Estendida' in v or 'Estendida' in sd,
                            'videoPath': vrel,
                            'posterPath': prel,
                            'sizeBytes': v_size,
                            'sizeFormatted': f'{v_size / (1024**3):.2f} GB' if v_size > 1024**3 else f'{v_size / (1024**2):.0f} MB',
                            'subtitles': v_subtitles,
                            'audio': v_audio['audio'],
                            'audioLabel': v_audio['audioLabel'],
                            'hasSubtitles': has_subs,
                            'overview': m_meta.get('overview', ''),
                            'cast': m_meta.get('cast', []),
                            'director': m_meta.get('director', ''),
                            'genres': m_meta.get('genres', []),
                            'rating': m_meta.get('rating', 7.5),
                            'tmdbUrl': m_meta.get('tmdbUrl', ''),
                            'imdbUrl': m_meta.get('imdbUrl', '')
                        })
            else:
                # Filme Avulso
                files = sorted(os.listdir(ipath))
                videos = [f for f in files if f.lower().endswith(('.mkv', '.mp4'))]
                posters = [f for f in files if f.lower() == 'poster.jpg']
                
                rel_prefix = f'../media/filmes/{item}'
                v_subtitles = parse_subtitles_for_dir(ipath, rel_prefix, subtitles_db)
                
                for v in videos:
                    vrel = f'{rel_prefix}/{v}'.replace('\\', '/')
                    prel = f'{rel_prefix}/poster.jpg'.replace('\\', '/') if posters else ''
                    full_vpath = os.path.join(ipath, v)
                    v_size = os.path.getsize(full_vpath)
                    v_audio = probe_audio_and_subs(full_vpath, audio_cache)
                    has_subs = bool(len(v_subtitles) > 0 or v_audio.get('hasEmbeddedSubtitles'))
                    m_title = clean_title(v) or clean_title(item)
                    m_year = get_year(v) or get_year(item)
                    m_meta = get_movie_info(m_title, year=m_year, franchise=None)
                    
                    movies_catalog.append({
                        'id': f'mov_{len(movies_catalog)+1}',
                        'type': 'movie',
                        'title': m_title,
                        'rawName': v,
                        'franchise': None,
                        'sequence': None,
                        'folder': item,
                        'year': m_year,
                        'resolution': get_resolution(v),
                        'format': os.path.splitext(v)[1][1:].upper(),
                        'isExtended': 'Versão Estendida' in v,
                        'videoPath': vrel,
                        'posterPath': prel,
                        'sizeBytes': v_size,
                        'sizeFormatted': f'{v_size / (1024**3):.2f} GB' if v_size > 1024**3 else f'{v_size / (1024**2):.0f} MB',
                        'subtitles': v_subtitles,
                        'audio': v_audio['audio'],
                        'audioLabel': v_audio['audioLabel'],
                        'hasSubtitles': has_subs,
                        'overview': m_meta.get('overview', ''),
                        'cast': m_meta.get('cast', []),
                        'director': m_meta.get('director', ''),
                        'genres': m_meta.get('genres', []),
                        'rating': m_meta.get('rating', 7.5),
                        'tmdbUrl': m_meta.get('tmdbUrl', ''),
                        'imdbUrl': m_meta.get('imdbUrl', '')
                    })
                    
    # -------------------------------------------------------------
    # 2. PROCESSAR SÉRIES (media/series)
    # -------------------------------------------------------------
    if os.path.exists(SERIES_DIR):
        for item in sorted(os.listdir(SERIES_DIR)):
            ipath = os.path.join(SERIES_DIR, item)
            if not os.path.isdir(ipath) or item.startswith('.'):
                continue
            
            series_poster = f'../media/series/{item}/poster.jpg'.replace('\\', '/') if os.path.exists(os.path.join(ipath, 'poster.jpg')) else ''
            season_dirs = [d for d in sorted(os.listdir(ipath)) if os.path.isdir(os.path.join(ipath, d)) and ('season' in d.lower() or 'temporada' in d.lower())]
            
            seasons_data = []
            total_episodes_count = 0
            
            for sd in season_dirs:
                sd_path = os.path.join(ipath, sd)
                season_poster = f'../media/series/{item}/{sd}/poster.jpg'.replace('\\', '/') if os.path.exists(os.path.join(sd_path, 'poster.jpg')) else series_poster
                
                m_season = re.search(r'(?:Season|Temporada)\s*0*(\d+)', sd, re.IGNORECASE)
                season_num = int(m_season.group(1)) if m_season else 1
                
                ep_files = [f for f in sorted(os.listdir(sd_path)) if f.lower().endswith(('.mkv', '.mp4'))]
                episodes = []
                
                rel_prefix = f'../media/series/{item}/{sd}'
                season_subs = parse_subtitles_for_dir(sd_path, rel_prefix, subtitles_db)
                
                for ep_file in ep_files:
                    total_episodes_count += 1
                    ep_size = os.path.getsize(os.path.join(sd_path, ep_file))
                    m_ep = re.search(r'[eE](?:pisode)?\s*0*(\d+)', ep_file)
                    if not m_ep:
                        m_ep = re.search(r'(\d+)x(\d+)', ep_file)
                        ep_num = int(m_ep.group(2)) if m_ep else total_episodes_count
                    else:
                        ep_num = int(m_ep.group(1))
                    
                    # Legendas específicas do episódio (mesmo nome do arquivo de vídeo ou código de episódio)
                    ep_base = os.path.splitext(ep_file)[0]
                    ep_subs = [s for s in season_subs if ep_base in s['filename']]
                    if not ep_subs:
                        m_code = re.search(r'[sS]\d+[eE]\d+|[eE]\d+', ep_file)
                        if m_code:
                            code = m_code.group(0).lower()
                            ep_subs = [s for s in season_subs if code in s['filename'].lower()]
                    if not ep_subs and len(season_subs) == 1:
                        ep_subs = season_subs
                    
                    full_ep_path = os.path.join(sd_path, ep_file)
                    ep_audio = probe_audio_and_subs(full_ep_path, audio_cache)
                    has_ep_subs = bool(len(ep_subs) > 0 or ep_audio.get('hasEmbeddedSubtitles'))
                    
                    episodes.append({
                        'id': f'ser_{len(series_catalog)+1}_s{season_num}_e{ep_num}',
                        'episodeNumber': ep_num,
                        'title': f'Episódio {ep_num}',
                        'rawName': ep_file,
                        'videoPath': f'{rel_prefix}/{ep_file}'.replace('\\', '/'),
                        'posterPath': season_poster or series_poster,
                        'resolution': get_resolution(ep_file),
                        'format': os.path.splitext(ep_file)[1][1:].upper(),
                        'sizeBytes': ep_size,
                        'sizeFormatted': f'{ep_size / (1024**3):.2f} GB' if ep_size > 1024**3 else f'{ep_size / (1024**2):.0f} MB',
                        'subtitles': ep_subs,
                        'audio': ep_audio['audio'],
                        'audioLabel': ep_audio['audioLabel'],
                        'hasSubtitles': has_ep_subs
                    })
                    
                seasons_data.append({
                    'seasonNumber': season_num,
                    'title': f'Temporada {season_num}',
                    'posterPath': season_poster,
                    'episodes': episodes
                })
                
            SERIES_YEARS = {
                'adolescence': 2025,
                'arcane': 2021,
                'chernobyl': 2019,
                'cyberpunk': 2022,
                'loki': 2021,
                'percy jackson': 2023,
                'pluribus': 2025,
                'severance': 2022,
                'the bear': 2022,
                'wandavision': 2021
            }
            s_info = get_series_info(item)
            s_year = s_info.get('year') or SERIES_YEARS.get(item.lower(), get_year(item))
            
            all_ep_audios = [ep['audio'] for s in seasons_data for ep in s['episodes']]
            all_ep_subs = [ep['hasSubtitles'] for s in seasons_data for ep in s['episodes']]
            if 'DUAL' in all_ep_audios:
                series_audio = 'DUAL'
                series_audio_label = 'Dual Áudio'
            elif 'DUB' in all_ep_audios and 'LEG' not in all_ep_audios:
                series_audio = 'DUB'
                series_audio_label = 'Dublado'
            elif 'LEG' in all_ep_audios:
                series_audio = 'LEG'
                series_audio_label = 'Legendado'
            else:
                series_audio = 'DUB'
                series_audio_label = 'Dublado'
            series_has_subs = any(all_ep_subs)
            SERIES_FRANCHISE = {
                'loki': ('Marvel', 9),
                'wandavision': ('Marvel', 10)
            }
            s_franchise = None
            s_sequence = None
            if item.lower() in SERIES_FRANCHISE:
                s_franchise, s_sequence = SERIES_FRANCHISE[item.lower()]
                
            series_catalog.append({
                'id': f'ser_{len(series_catalog)+1}',
                'type': 'series',
                'title': s_info.get('title') or item,
                'rawName': item,
                'folder': item,
                'franchise': s_franchise,
                'sequence': s_sequence,
                'year': s_year,
                'posterPath': series_poster,
                'totalSeasons': len(seasons_data),
                'totalEpisodes': total_episodes_count,
                'audio': series_audio,
                'audioLabel': series_audio_label,
                'hasSubtitles': series_has_subs,
                'overview': s_info.get('overview', ''),
                'cast': s_info.get('cast', []),
                'creator': s_info.get('creator', ''),
                'genres': s_info.get('genres', []),
                'rating': s_info.get('rating', 8.0),
                'tmdbUrl': s_info.get('tmdbUrl', ''),
                'imdbUrl': s_info.get('imdbUrl', ''),
                'seasons': seasons_data
            })
            
    # Salvar cache persistente de áudio para execuções instantâneas
    save_audio_cache(audio_cache)
    
    # Catálogo unificado para a Home (Filmes + Séries como cards de primeiro nível)
    unified_catalog = list(movies_catalog) + list(series_catalog)
    
    output_js = os.path.join(APP_DIR, 'catalogo.js')
    with open(output_js, 'w', encoding='utf-8') as out:
        out.write('// Catálogo gerado automaticamente pelo CineLocal\n')
        out.write('window.CATALOGO = ')
        json.dump(unified_catalog, out, ensure_ascii=False, indent=2)
        out.write(';\n\n')
        out.write('window.CATALOGO_FILMES = ')
        json.dump(movies_catalog, out, ensure_ascii=False, indent=2)
        out.write(';\n\n')
        out.write('window.CATALOGO_SERIES = ')
        json.dump(series_catalog, out, ensure_ascii=False, indent=2)
        out.write(';\n\n')
        out.write('window.LEGENDAS_DB = ')
        json.dump(subtitles_db, out, ensure_ascii=False)
        out.write(';\n')
        
    print(f'Sucesso: Catálogo CineLocal atualizado com {len(movies_catalog)} filmes, {len(series_catalog)} séries e {len(subtitles_db)} legendas!')
    return {
        'catalog': unified_catalog,
        'movies': movies_catalog,
        'series': series_catalog
    }

if __name__ == '__main__':
    build_catalog()

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
from atualizar_catalogo import build_catalog

PORT = 8000
APP_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_DIR = os.path.dirname(APP_DIR)
PORTABLE_VLC = os.path.join(APP_DIR, "vlc", "vlc.exe")
SYSTEM_VLC = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

AUDIO_CACHE = {}

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

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # Redireciona a raiz para a aplicação CineLocal
        if parsed.path in ('/', '', '/index.html'):
            self.send_response(302)
            self.send_header('Location', '/app/index.html')
            self.end_headers()
            return
            
        if parsed.path.startswith('/CineLocal/'):
            self.send_response(301)
            self.send_header('Location', parsed.path.replace('/CineLocal/', '/app/'))
            self.end_headers()
            return
            
        # API de recursos do ambiente (VLC e FFmpeg disponíveis)
        if parsed.path in ('/api/capabilities', '/api/status'):
            vlc_bin = get_vlc_path()
            ffmpeg_bin = get_ffmpeg_bin()
            data = json.dumps({
                "vlcAvailable": bool(vlc_bin),
                "vlcPath": vlc_bin or "",
                "ffmpegAvailable": bool(ffmpeg_bin),
                "ffmpegPath": ffmpeg_bin or ""
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
        
        ctype = self.guess_type(path)
        if path.lower().endswith('.mkv'):
            ctype = 'video/x-matroska'
        elif path.lower().endswith('.mp4'):
            ctype = 'video/mp4'
        elif path.lower().endswith('.srt'):
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

def run():
    print("Verificando e sincronizando catálogo CineLocal...")
    try:
        build_catalog()
    except Exception as e:
        print(f"Aviso ao compilar catálogo: {e}")
    
    local_ip = get_local_ip()
    local_url = f'http://localhost:{PORT}/'
    tv_url = f'http://{local_ip}:{PORT}/'
    
    vlc_bin = get_vlc_path()
    ffmpeg_bin = get_ffmpeg_bin()
    vlc_status = f"Detectado ({vlc_bin})" if vlc_bin else "Nao detectado (Opcional - codecs TrueHD/DTS)"
    ffmpeg_status = f"Detectado ({ffmpeg_bin})" if ffmpeg_bin else "Nao detectado (Opcional - analise de audio)"

    banner = f"""
================================================================================
           CINELOCAL - SERVIDOR DE STREAMING ATIVO (MULTITHREAD)
================================================================================

  > No seu Computador:   {local_url}
  > Na sua Smart TV:     {tv_url}
  > No Celular / Tablet: {tv_url}

  - Streaming HTTP 206 (Seek fluido em 4K e 1080p)
  - Player Web Nativo com Volume Boost ate 200%
  - VLC Media Player: {vlc_status}
  - FFmpeg:           {ffmpeg_status}

  Pressione Ctrl + C no terminal para encerrar o servidor.
================================================================================
"""
    print(banner)
    
    try:
        webbrowser.open(local_url)
    except Exception:
        pass
    
    with ThreadingServer(('0.0.0.0', PORT), CineLocalStreamingHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado. Bom filme!")

if __name__ == '__main__':
    run()

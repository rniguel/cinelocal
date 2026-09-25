# -*- coding: utf-8 -*-
"""
CineLocal - Otimizador de Áudio para Navegador e Smart TV
Injeta faixa AAC estéreo compatível com Chrome/Edge/Firefox/Smart TV nos MKVs,
mantendo o vídeo 100% original (cópia sem perdas, 0% CPU de vídeo)
e preservando todas as trilhas originais de cinema (TrueHD Atmos 7.1, AC3 5.1).
"""

import os
import sys
import subprocess
import time
import re
from atualizar_catalogo import build_catalog

try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

APP_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_DIR = os.path.dirname(APP_DIR)
FFMPEG_BIN = os.path.join(APP_DIR, "bin", "ffmpeg.exe")

def get_mkv_streams(filepath):
    res = subprocess.run([FFMPEG_BIN, "-i", filepath], capture_output=True, text=True, encoding="utf-8", errors="ignore")
    lines = res.stderr.split("\n")
    
    audio_streams = []
    video_streams = []
    
    for l in lines:
        m = re.search(r"Stream #0:(\d+)(?:\(([a-zA-Z]+)\))?.*?: (Video|Audio): (.*)", l)
        if m:
            st_idx = int(m.group(1))
            lang = (m.group(2) or "und").lower()
            st_type = m.group(3)
            rest = m.group(4)
            codec = rest.split()[0].rstrip(',').lower()
            
            info = {
                "index": st_idx,
                "lang": lang,
                "codec": codec,
                "raw": rest,
                "is_default": "default" in l.lower()
            }
            if st_type == "Audio":
                audio_streams.append(info)
            elif st_type == "Video":
                video_streams.append(info)
                
    return video_streams, audio_streams

def needs_web_audio(audio_streams):
    if not audio_streams:
        return False, None
    first = audio_streams[0]
    # Se o primeiro áudio já for aac, mp3 ou opus, o navegador toca perfeitamente
    if first["codec"] in ("aac", "mp3", "opus"):
        return False, None
        
    # Encontra a melhor trilha para converter em AAC (preferencialmente português)
    por_tracks = [a for a in audio_streams if a["lang"] in ("por", "pob", "pt", "bra")]
    if por_tracks:
        best_track = por_tracks[0]
    else:
        best_track = audio_streams[0]
        
    return True, best_track

def process_file(filepath):
    rel_path = os.path.relpath(filepath, MOVIES_DIR)
    v_streams, a_streams = get_mkv_streams(filepath)
    
    needed, best_audio = needs_web_audio(a_streams)
    if not needed:
        return False, f"Já compatível: {rel_path}"
        
    orig_size = os.path.getsize(filepath)
    dir_name = os.path.dirname(filepath)
    base_name = os.path.basename(filepath)
    temp_filepath = os.path.join(dir_name, base_name + ".temp.mkv")
    
    # Monta comando FFmpeg:
    # 1. Copia vídeo
    # 2. Injeta AAC estéreo (192kbps) como faixa padrão #0
    # 3. Copia todas as faixas de áudio originais (TrueHD Atmos, AC3 5.1, etc.)
    # 4. Copia todas as legendas embutidas
    cmd = [
        FFMPEG_BIN,
        "-y",
        "-nostdin",
        "-nostats",
        "-loglevel", "error",
        "-i", filepath,
        "-map", "0:v:0",
        "-c:v", "copy",
        "-map", f"0:{best_audio['index']}",
        "-map", "0:a",
        "-c:a", "copy",
        "-c:a:0", "aac",
        "-b:a:0", "192k",
        "-ac:a:0", "2",
        "-metadata:s:a:0", f"title={best_audio['lang'].upper()} [AAC Web]",
        "-metadata:s:a:0", f"language={best_audio['lang']}",
        "-disposition:a:0", "default"
    ]
    
    # Remove a flag default das faixas originais para que o navegador priorize a faixa AAC
    for idx in range(1, len(a_streams) + 1):
        cmd.extend([f"-disposition:a:{idx}", "0"])
        
    cmd.extend([
        "-map", "0:s?",
        "-c:s", "copy",
        temp_filepath
    ])
    
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    stderr_out, _ = proc.communicate()
    
    if proc.returncode != 0 or not os.path.exists(temp_filepath):
        err_msg = stderr_out.strip() if stderr_out else "Erro desconhecido"
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        return False, f"Erro ao converter: {rel_path} ({err_msg})"
        
    temp_size = os.path.getsize(temp_filepath)
    # Validação de segurança: temp_size deve ser pelo menos 90% do original
    if temp_size < orig_size * 0.90:
        os.remove(temp_filepath)
        return False, f"Tamanho inconsistente ({temp_size} vs {orig_size}): {rel_path}"
        
    # Substituição atômica segura
    os.replace(temp_filepath, filepath)
    elapsed = time.time() - t0
    return True, f"Otimizado com sucesso em {elapsed:.1f}s: {rel_path}"

def main():
    if not os.path.exists(FFMPEG_BIN):
        print(f"Erro: FFmpeg não encontrado em {FFMPEG_BIN}")
        return
        
    print("=" * 70)
    print("      CINELOCAL - OTIMIZADOR DE ÁUDIO PARA NAVEGADOR E SMART TV")
    print("=" * 70)
    print("Escaneando biblioteca de filmes...")
    
    media_folder = os.path.join(MOVIES_DIR, "media")
    mkv_files = []
    scan_target = media_folder if os.path.exists(media_folder) else MOVIES_DIR
    for root, dirs, files in os.walk(scan_target):
        if "app" in root or "CineLocal" in root or ".gemini" in root:
            continue
        for f in files:
            if f.lower().endswith('.mkv'):
                mkv_files.append(os.path.join(root, f))
                
    mkv_files.sort()
    
    targets = []
    for p in mkv_files:
        v, a = get_mkv_streams(p)
        needed, best = needs_web_audio(a)
        if needed:
            targets.append((p, best))
            
    total = len(targets)
    print(f"Total de filmes MKV que necessitam de trilha AAC Web: {total}\n")
    
    if total == 0:
        print("Todos os filmes já possuem compatibilidade nativa com o navegador!")
        return
        
    success_count = 0
    for i, (p, best) in enumerate(targets, 1):
        rel = os.path.relpath(p, MOVIES_DIR)
        print(f"[{i}/{total}] Processando: {rel} (Base: #{best['index']} {best['lang']}:{best['codec']})...")
        ok, msg = process_file(p)
        if ok:
            print(f"       -> {msg}")
            success_count += 1
        else:
            print(f"       -> [AVISO] {msg}")
            
    print("\n" + "=" * 70)
    print(f"Concluído! {success_count} de {total} filmes otimizados para reprodução no navegador.")
    print("Atualizando catálogo do CineLocal...")
    build_catalog()
    print("Catálogo pronto e atualizado!")
    print("=" * 70)

if __name__ == '__main__':
    main()

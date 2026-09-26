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
import shutil

# Ensure APP_DIR is in sys.path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from atualizar_catalogo import build_catalog, get_ffmpeg_bin

try:
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')
except Exception:
    pass

MOVIES_DIR = os.path.dirname(APP_DIR)

def format_size(bytes_val):
    if bytes_val >= 1024 ** 3:
        return f"{bytes_val / (1024 ** 3):.2f} GB"
    elif bytes_val >= 1024 ** 2:
        return f"{bytes_val / (1024 ** 2):.1f} MB"
    return f"{bytes_val / 1024:.0f} KB"

def format_duration(seconds):
    if not seconds or seconds <= 0:
        return "Desconhecida"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}h {m:02d}m"
    return f"{m}m {s:02d}s"

def format_eta(seconds):
    if seconds <= 0:
        return "concluindo..."
    m = int(seconds // 60)
    s = int(seconds % 60)
    if m > 0:
        return f"~{m}m {s:02d}s"
    return f"~{s}s"

def get_progress_bar(current, total, width=20):
    pct = current / total if total > 0 else 1.0
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {int(pct * 100)}%"

def get_mkv_details(filepath, ffmpeg_bin):
    """Extrai trilhas de áudio, vídeo e duração total do arquivo."""
    try:
        res = subprocess.run(
            [ffmpeg_bin, "-i", filepath],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        lines = res.stderr.split("\n")
    except Exception:
        return [], [], 0

    audio_streams = []
    video_streams = []
    duration_secs = 0
    
    for l in lines:
        if "Duration:" in l:
            m_dur = re.search(r"Duration:\s*(\d{2}):(\d{2}):(\d{2})", l)
            if m_dur:
                duration_secs = int(m_dur.group(1)) * 3600 + int(m_dur.group(2)) * 60 + int(m_dur.group(3))

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
                
    return video_streams, audio_streams, duration_secs

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

def process_file(filepath, ffmpeg_bin, best_audio, duration_secs):
    rel_path = os.path.relpath(filepath, MOVIES_DIR).replace('\\', '/')
    orig_size = os.path.getsize(filepath)
    dir_name = os.path.dirname(filepath)
    base_name = os.path.basename(filepath)
    temp_filepath = os.path.join(dir_name, base_name + ".temp.mkv")
    
    _, a_streams, _ = get_mkv_details(filepath, ffmpeg_bin)
    
    # Monta comando FFmpeg:
    # 1. Copia vídeo 100% sem perdas (copy)
    # 2. Injeta AAC estéreo (192kbps) como faixa padrão #0
    # 3. Preserva todas as faixas originais de áudio (TrueHD Atmos, DTS, AC3)
    # 4. Preserva todas as legendas embutidas
    cmd = [
        ffmpeg_bin,
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
    
    for idx in range(1, len(a_streams) + 1):
        cmd.extend([f"-disposition:a:{idx}", "0"])
        
    cmd.extend([
        "-map", "0:s?",
        "-c:s", "copy",
        temp_filepath
    ])
    
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    stderr_out, _ = proc.communicate()
    elapsed = time.time() - t0
    
    if proc.returncode != 0 or not os.path.exists(temp_filepath):
        err_msg = stderr_out.strip() if stderr_out else "Erro desconhecido"
        if os.path.exists(temp_filepath):
            try:
                os.remove(temp_filepath)
            except Exception:
                pass
        return False, f"Falha na conversão ({err_msg})", elapsed
        
    temp_size = os.path.getsize(temp_filepath)
    # Validação de integridade: temp_size deve ser pelo menos 90% do original
    if temp_size < orig_size * 0.90:
        if os.path.exists(temp_filepath):
            try:
                os.remove(temp_filepath)
            except Exception:
                pass
        return False, f"Tamanho inconsistente ({format_size(temp_size)} vs original {format_size(orig_size)})", elapsed
        
    # Substituição atômica segura
    os.replace(temp_filepath, filepath)
    
    speed_x = (duration_secs / elapsed) if (duration_secs > 0 and elapsed > 0) else 0
    speed_str = f" • {speed_x:.0f}x tempo real" if speed_x > 0 else ""
    return True, f"Concluído em {elapsed:.1f}s{speed_str} ({format_size(temp_size)})", elapsed

def main():
    ffmpeg_bin = get_ffmpeg_bin()
    
    print("\n" + "=" * 76)
    print("      🎬 CINELOCAL - OTIMIZADOR DE ÁUDIO WEB (CHROME / SMART TV)")
    print("=" * 76)
    
    if not ffmpeg_bin:
        print("\n❌ [ERRO] FFmpeg não encontrado!")
        print("   Para converter áudio para navegadores e Smart TVs, o FFmpeg é necessário.")
        print("   • Baixe em: https://ffmpeg.org/download.html")
        print("   • Ou instale via PowerShell: winget install Gyan.FFmpeg")
        print("=" * 76 + "\n")
        return
        
    print(f"⚙️  FFmpeg detectado: {ffmpeg_bin}")
    print("🔍 Escaneando biblioteca de filmes em busca de faixas de cinema sem AAC...\n")
    
    media_folder = os.path.join(MOVIES_DIR, "media")
    scan_target = media_folder if os.path.exists(media_folder) else MOVIES_DIR
    
    mkv_files = []
    for root, dirs, files in os.walk(scan_target):
        if any(skip in root for skip in ("app", "CineLocal", ".gemini", ".git")):
            continue
        for f in files:
            if f.lower().endswith('.mkv'):
                mkv_files.append(os.path.join(root, f))
                
    mkv_files.sort()
    
    targets = []
    for p in mkv_files:
        v, a, dur = get_mkv_details(p, ffmpeg_bin)
        needed, best = needs_web_audio(a)
        if needed:
            targets.append({
                "path": p,
                "best_audio": best,
                "duration": dur,
                "size": os.path.getsize(p)
            })
            
    total = len(targets)
    
    if total == 0:
        print("✨ [PARABÉNS] Todos os filmes da sua biblioteca já possuem áudio AAC compatível!")
        print("   Seus vídeos tocarão com som diretamente no Chrome, Edge, Celular e Smart TV.")
        print("=" * 76 + "\n")
        return
        
    total_size_bytes = sum(t["size"] for t in targets)
    print(f"🎯 Total de filmes a otimizar: {total} ({format_size(total_size_bytes)})")
    print("⚡ Processo 100% lossless: O vídeo não é recodificado (0% perda de qualidade).")
    print("-" * 76)
    
    success_count = 0
    total_time_spent = 0.0
    
    for i, item in enumerate(targets, 1):
        p = item["path"]
        best = item["best_audio"]
        dur = item["duration"]
        size_str = format_size(item["size"])
        dur_str = format_duration(dur)
        rel_path = os.path.relpath(p, MOVIES_DIR).replace('\\', '/')
        
        # Estimativa de tempo restante (ETA)
        if i > 1 and success_count > 0:
            avg_per_file = total_time_spent / success_count
            remaining_files = total - (i - 1)
            eta_str = format_eta(avg_per_file * remaining_files)
        else:
            eta_str = "calculando..."
            
        progress = get_progress_bar(i - 1, total)
        
        print(f"\n[{i}/{total}] {progress} • Estimativa restante: {eta_str}")
        print(f"🎬 Filme:    {rel_path}")
        print(f"📊 Info:     Tamanho: {size_str} • Duração: {dur_str}")
        print(f"🔊 Origem:   Trilha #{best['index']} ({best['lang'].upper()} - {best['codec'].upper()}) ➔ Injetando AAC 2.0 Web")
        print(f"⏳ Processando...")
        
        ok, msg, elapsed = process_file(p, ffmpeg_bin, best, dur)
        total_time_spent += elapsed
        
        if ok:
            print(f"✅ Status:   {msg}")
            success_count += 1
        else:
            print(f"⚠️ Aviso:    {msg}")
            
    print("\n" + "=" * 76)
    avg_speed = (total_time_spent / success_count) if success_count > 0 else 0
    print(f"🎉 OTIMIZAÇÃO CONCLUÍDA EM {total_time_spent:.1f}s!")
    print(f"   • Filmes otimizados com sucesso: {success_count} de {total}")
    print(f"   • Média por filme:               {avg_speed:.1f}s")
    print(f"   • Áudio estéreo AAC:             Injetado como padrão para Web e TV")
    print(f"   • Áudios originais (TrueHD/DTS): 100% preservados para uso com VLC")
    print("-" * 76)
    print("🔄 Sincronizando metadados do CineLocal...")
    build_catalog()
    print("✅ Catálogo atualizado com as novas faixas!")
    print("=" * 76 + "\n")

if __name__ == '__main__':
    main()

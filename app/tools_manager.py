# -*- coding: utf-8 -*-
"""
Módulo de Ferramentas e Rotinas Unificadas do CineLocal (Issue #17)
Centraliza atualização de catálogo, enriquecimento TMDb/Cinemeta e otimização de áudio web.
"""

import os
import sys
import json
import time
import threading
import urllib.request
import urllib.parse
import re

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)
MEDIA_DIR = os.path.join(ROOT_DIR, "media")
FILMES_DIR = os.path.join(MEDIA_DIR, "filmes")
SERIES_DIR = os.path.join(MEDIA_DIR, "series")
TMDB_CACHE_FILE = os.path.join(APP_DIR, "tmdb_metadata_cache.json")

TOOLS_STATE = {
    "catalog": {"running": False, "message": "Pronto", "lastUpdated": None, "moviesCount": 0, "seriesCount": 0},
    "tmdb": {"running": False, "message": "Pronto", "processed": 0, "total": 0, "currentTitle": ""},
    "audio": {"running": False, "message": "Pronto", "processed": 0, "total": 0, "currentFile": ""}
}

def run_catalog_update():
    """Executa a atualização do catálogo e cache de mídias."""
    if TOOLS_STATE["catalog"]["running"]:
        return {"success": False, "message": "Atualização já em andamento"}

    def _worker():
        TOOLS_STATE["catalog"]["running"] = True
        TOOLS_STATE["catalog"]["message"] = "Escaneando mídias e atualizando índices..."
        try:
            from atualizar_catalogo import build_catalog
            result = build_catalog()
            movies = result.get('movies', [])
            series = result.get('series', [])
            TOOLS_STATE["catalog"]["moviesCount"] = len(movies)
            TOOLS_STATE["catalog"]["seriesCount"] = len(series)
            TOOLS_STATE["catalog"]["lastUpdated"] = time.strftime("%H:%M:%S")
            TOOLS_STATE["catalog"]["message"] = f"Concluído: {len(movies)} filmes e {len(series)} séries indexados."
        except Exception as e:
            TOOLS_STATE["catalog"]["message"] = f"Erro ao atualizar: {e}"
        finally:
            TOOLS_STATE["catalog"]["running"] = False

    th = threading.Thread(target=_worker, daemon=True)
    th.start()
    return {"success": True, "message": "Varredura iniciada em segundo plano"}

def run_tmdb_enricher(api_key=""):
    """Executa busca de sinopses e metadados no TMDb/Cinemeta."""
    if TOOLS_STATE["tmdb"]["running"]:
        return {"success": False, "message": "Busca de metadados já em andamento"}

    def _worker():
        TOOLS_STATE["tmdb"]["running"] = True
        TOOLS_STATE["tmdb"]["message"] = "Identificando títulos locais..."
        TOOLS_STATE["tmdb"]["processed"] = 0

        # Carrega cache existente
        cache = {}
        if os.path.exists(TMDB_CACHE_FILE):
            try:
                with open(TMDB_CACHE_FILE, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
            except Exception:
                cache = {}

        # Coleta filmes
        items = []
        if os.path.exists(FILMES_DIR):
            for root, dirs, files in os.walk(FILMES_DIR):
                video_files = [f for f in files if f.lower().endswith(('.mkv', '.mp4', '.avi', '.webm'))]
                if video_files:
                    folder_name = os.path.basename(root)
                    items.append((root, folder_name))

        TOOLS_STATE["tmdb"]["total"] = len(items)

        for idx, (root, folder_name) in enumerate(items):
            TOOLS_STATE["tmdb"]["processed"] = idx + 1
            TOOLS_STATE["tmdb"]["currentTitle"] = folder_name
            clean_title = re.sub(r'\s*\(\d{4}\).*', '', folder_name).strip()
            clean_title = re.sub(r'^\d+\s*-\s*', '', clean_title).strip()
            cache_key = f"movie_{clean_title}"

            if cache_key in cache:
                continue

            # Busca no Cinemeta (sem necessidade de API key)
            try:
                search_url = f"https://v3-cinemeta.strem.io/catalog/movie/top/search={urllib.parse.quote(clean_title)}.json"
                req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (CineLocal/2.5)'})
                with urllib.request.urlopen(req, timeout=5) as res:
                    data = json.loads(res.read().decode('utf-8'))
                    metas = data.get('metas', [])
                    if metas:
                        top = metas[0]
                        cache[cache_key] = {
                            "title": top.get('name', clean_title),
                            "overview": top.get('description', ''),
                            "rating": top.get('imdbRating', 'N/A'),
                            "year": top.get('year', ''),
                            "genres": top.get('genres', []),
                            "poster": top.get('poster', ''),
                            "imdb_id": top.get('id', '')
                        }
                        # Baixa poster se não existir
                        poster_file = os.path.join(root, 'poster.jpg')
                        if not os.path.exists(poster_file) and top.get('poster'):
                            try:
                                p_req = urllib.request.Request(top.get('poster'), headers={'User-Agent': 'Mozilla/5.0 (CineLocal/2.5)'})
                                with urllib.request.urlopen(p_req, timeout=8) as p_res:
                                    with open(poster_file, 'wb') as pf:
                                        pf.write(p_res.read())
                            except Exception:
                                pass
                time.sleep(0.3)
            except Exception:
                pass

        # Salva cache
        try:
            with open(TMDB_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        TOOLS_STATE["tmdb"]["message"] = f"Metadados enriquecidos para {len(items)} títulos."
        TOOLS_STATE["tmdb"]["running"] = False

    th = threading.Thread(target=_worker, daemon=True)
    th.start()
    return {"success": True, "message": "Enriquecimento de metadados iniciado em segundo plano"}

def run_audio_optimizer():
    """Varre e otimiza áudio web para compatibilidade nativa."""
    if TOOLS_STATE["audio"]["running"]:
        return {"success": False, "message": "Otimização de áudio já em andamento"}

    def _worker():
        TOOLS_STATE["audio"]["running"] = True
        TOOLS_STATE["audio"]["message"] = "Escaneando arquivos de vídeo..."
        try:
            from otimizar_audio_web import main as audio_main
            # Executa rotina de áudio
            audio_main()
            TOOLS_STATE["audio"]["message"] = "Varredura e otimização de áudio concluídas com sucesso."
        except Exception as e:
            TOOLS_STATE["audio"]["message"] = f"Erro na otimização de áudio: {e}"
        finally:
            TOOLS_STATE["audio"]["running"] = False

    th = threading.Thread(target=_worker, daemon=True)
    th.start()
    return {"success": True, "message": "Otimizador de áudio iniciado em segundo plano"}

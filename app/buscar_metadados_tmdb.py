# -*- coding: utf-8 -*-
"""
CineLocal - Enriquecedor e Rastreador Automático de Metadados TMDb
===================================================================
Utilitário DESACOPLADO e OPCIONAL para buscar sinopses oficiais em pt-BR,
notas do IMDb/TMDb, elenco, direção e pôsteres em alta definição.

REGRAS DE SEGURANÇA:
1. NUNCA renomeia, altera ou deleta arquivos de vídeo.
2. Se a pasta já possuir 'poster.jpg', o pôster existente é mantido intacto.
3. Opera 100% com a biblioteca padrão do Python (sem dependência de pip).
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(ROOT_DIR, 'media')
FILMES_DIR = os.path.join(MEDIA_DIR, 'filmes')
SERIES_DIR = os.path.join(MEDIA_DIR, 'series')
CACHE_FILE = os.path.join(ROOT_DIR, 'app', 'tmdb_metadata_cache.json')

# Padrões para limpeza de títulos de arquivos de mídia
CLEAN_PATTERNS = [
    r'(?i)\b(?:1080p|720p|2160p|4k|uhd|bluray|blu-ray|web-dl|webrip|hdtv|dvdrip|remux)\b',
    r'(?i)\b(?:x264|x265|hevc|h264|h265|avc|10bit|aac|ac3|dts|dts-hd|truehd|ddp5\.1|atmos)\b',
    r'(?i)\b(?:dual|dublado|legendado|multi|cinelocal|bludv|comandotorrents|yts|yify|rarbg)\b',
    r'(?i)\b(?:versao estendida|extended|imax|directors cut|remastered)\b',
    r'[\[\]\(\)]',
    r'[._]'
]

def clean_movie_title(raw_name):
    name = raw_name
    for pat in CLEAN_PATTERNS:
        name = re.sub(pat, ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def extract_year(text):
    m = re.search(r'\b(19\d{2}|20\d{2})\b', text)
    return int(m.group(1)) if m else None

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def search_tmdb_movie(api_key, query, year=None):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": query,
        "language": "pt-BR",
        "include_adult": "false"
    }
    if year:
        params["year"] = str(year)
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "CineLocal/2.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        results = data.get('results', [])
        return results[0] if results else None

def search_tmdb_series(api_key, query, year=None):
    base_url = "https://api.themoviedb.org/3/search/tv"
    params = {
        "api_key": api_key,
        "query": query,
        "language": "pt-BR",
        "include_adult": "false"
    }
    if year:
        params["first_air_date_year"] = str(year)
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "CineLocal/2.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        results = data.get('results', [])
        return results[0] if results else None

def download_poster(image_path, target_file):
    if not image_path:
        return False
    url = f"https://image.tmdb.org/t/p/w500{image_path}"
    req = urllib.request.Request(url, headers={"User-Agent": "CineLocal/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            with open(target_file, 'wb') as f:
                f.write(content)
        return True
    except Exception as e:
        print(f"   ⚠️ Falha ao baixar pôster ({url}): {e}")
        return False

def main():
    print("=" * 76)
    print("      🎬 CINELOCAL - ENRIQUECEDOR SEGURO DE METADADOS (TMDB)")
    print("=" * 76)
    print("🛡️  Modo Seguro: Nenhum arquivo de vídeo será tocado ou renomeado.")
    print("📁  Posters: Se 'poster.jpg' já existir na pasta, ele NÃO será substituído.")
    print("-" * 76)

    api_key = os.environ.get("TMDB_API_KEY", "").strip()
    if not api_key:
        print("💡 Para buscar metadados automaticamente no TMDb (The Movie Database):")
        print("   1. Crie uma conta gratuita em: https://www.themoviedb.org/signup")
        print("   2. Obtenha sua API Key v3 gratuita em: Configurações -> API")
        print("   3. Insira sua chave abaixo (ou defina a variável TMDB_API_KEY no Windows).\n")
        try:
            api_key = input("🔑 Digite sua chave de API do TMDb (ou Enter para sair): ").strip()
        except EOFError:
            api_key = ""

    if not api_key:
        print("\nℹ️  Operação cancelada. O CineLocal continuará utilizando os metadados locais.")
        return

    cache = load_cache()
    updated_count = 0
    poster_downloaded_count = 0

    print("\n🍿 [1/2] Verificando Catálogo de Filmes...")
    if os.path.exists(FILMES_DIR):
        for root, dirs, files in os.walk(FILMES_DIR):
            video_files = [f for f in files if f.lower().endswith(('.mkv', '.mp4', '.avi', '.webm'))]
            if not video_files:
                continue

            folder_name = os.path.basename(root)
            poster_path = os.path.join(root, 'poster.jpg')
            has_poster = os.path.exists(poster_path)

            extracted_year = extract_year(folder_name)
            clean_name = clean_movie_title(folder_name)
            if extracted_year:
                clean_name = clean_name.replace(str(extracted_year), '').strip()

            cache_key = f"movie_{clean_name}_{extracted_year}"
            print(f"   🔎 Analisando: '{clean_name}' ({extracted_year or 'S/A'})...", end="")

            if cache_key in cache:
                print(" [EM CACHE]")
                tmdb_data = cache[cache_key]
            else:
                try:
                    tmdb_data = search_tmdb_movie(api_key, clean_name, extracted_year)
                    if tmdb_data:
                        cache[cache_key] = tmdb_data
                        print(" [ENCONTRADO NO TMDB!]")
                        updated_count += 1
                    else:
                        print(" [NÃO ENCONTRADO]")
                except Exception as e:
                    print(f" [ERRO: {e}]")
                    tmdb_data = None

            if tmdb_data and not has_poster and tmdb_data.get('poster_path'):
                print(f"      ↳ Baixando pôster oficial para: {os.path.basename(root)}/poster.jpg...")
                if download_poster(tmdb_data['poster_path'], poster_path):
                    poster_downloaded_count += 1

    print("\n📺 [2/2] Verificando Catálogo de Séries...")
    if os.path.exists(SERIES_DIR):
        for item in os.listdir(SERIES_DIR):
            series_path = os.path.join(SERIES_DIR, item)
            if not os.path.isdir(series_path):
                continue

            poster_path = os.path.join(series_path, 'poster.jpg')
            has_poster = os.path.exists(poster_path)

            extracted_year = extract_year(item)
            clean_name = clean_movie_title(item)
            if extracted_year:
                clean_name = clean_name.replace(str(extracted_year), '').strip()

            cache_key = f"series_{clean_name}_{extracted_year}"
            print(f"   🔎 Analisando: '{clean_name}' ({extracted_year or 'S/A'})...", end="")

            if cache_key in cache:
                print(" [EM CACHE]")
                tmdb_data = cache[cache_key]
            else:
                try:
                    tmdb_data = search_tmdb_series(api_key, clean_name, extracted_year)
                    if tmdb_data:
                        cache[cache_key] = tmdb_data
                        print(" [ENCONTRADO NO TMDB!]")
                        updated_count += 1
                    else:
                        print(" [NÃO ENCONTRADO]")
                except Exception as e:
                    print(f" [ERRO: {e}]")
                    tmdb_data = None

            if tmdb_data and not has_poster and tmdb_data.get('poster_path'):
                print(f"      ↳ Baixando pôster oficial para: {item}/poster.jpg...")
                if download_poster(tmdb_data['poster_path'], poster_path):
                    poster_downloaded_count += 1

    save_cache(cache)
    print("\n" + "=" * 76)
    print("🎉 BUSCA CONCLUÍDA COM SUCESSO!")
    print(f"   • Metadados novos indexados: {updated_count}")
    print(f"   • Novos pôsteres baixados:   {poster_downloaded_count}")
    print(f"   • Base em cache:             app/tmdb_metadata_cache.json")
    print("=" * 76)
    print("💡 Dica: Agora execute 'python app/atualizar_catalogo.py' para carregar os dados no catálogo!")

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
Script de Empacotamento do CineLocal para Samsung Smart TV (Tizen OS)
Gera o pacote oficial .wgt (Widget Tizen) na pasta dist/
"""

import os
import sys
import shutil
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIZEN_SRC = os.path.join(BASE_DIR, "tizen")
DIST_DIR = os.path.join(BASE_DIR, "dist")
OUTPUT_WGT = os.path.join(DIST_DIR, "CineLocal.wgt")

def package_tizen_app():
    print("=" * 65)
    print("🎬 CINELOCAL - EMPACOTADOR PARA SAMSUNG SMART TV (TIZEN OS)")
    print("=" * 65)

    if not os.path.exists(TIZEN_SRC):
        print(f"❌ Erro: Diretório fonte '{TIZEN_SRC}' não encontrado!")
        sys.exit(1)

    config_file = os.path.join(TIZEN_SRC, "config.xml")
    if not os.path.exists(config_file):
        print("❌ Erro: config.xml ausente em tizen/!")
        sys.exit(1)

    os.makedirs(DIST_DIR, exist_ok=True)

    print(f"📁 Diretório Fonte: {TIZEN_SRC}")
    print(f"📦 Destino:         {OUTPUT_WGT}")
    print("-" * 65)

    # Cria o arquivo ZIP / WGT
    files_to_pack = []
    for root, _, files in os.walk(TIZEN_SRC):
        for f in files:
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, TIZEN_SRC)
            files_to_pack.append((fp, rel))

    print(f"📄 Empacotando {len(files_to_pack)} arquivo(s):")
    with zipfile.ZipFile(OUTPUT_WGT, 'w', zipfile.ZIP_DEFLATED) as z:
        for full_path, arc_name in files_to_pack:
            print(f"   ↳ {arc_name}")
            z.write(full_path, arc_name)

    size_kb = round(os.path.getsize(OUTPUT_WGT) / 1024, 1)
    print("-" * 65)
    print(f"✅ Pacote Tizen gerado com sucesso: {OUTPUT_WGT} ({size_kb} KB)")
    print("=" * 65)
    print("💡 Como instalar na Smart TV Samsung:")
    print("1. Ative o Developer Mode na TV (Apps -> 12345 -> Developer Mode ON)")
    print("2. Conecte pelo Tizen Studio ou Tizen CLI:")
    print(f"   tizen install -n CineLocal.wgt -t <IP_DA_TV>")
    print("=" * 65)

if __name__ == "__main__":
    package_tizen_app()

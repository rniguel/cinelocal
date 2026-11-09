# -*- coding: utf-8 -*-
"""
CineLocal - Validador de Integridade da Interface Web
=====================================================
A partir da Issue #8, o arquivo 'app/index.html' é a ÚNICA FONTE DA VERDADE
oficial para o frontend do CineLocal (HTML, CSS e JavaScript).

Este script agora atua como validador de integridade e compatibilidade,
evitando que o index.html seja sobrescrito por strings hardcoded.
"""

import os
import sys

# Configura encoding UTF-8 no terminal Windows para evitar UnicodeEncodeError
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

APP_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(APP_DIR, "index.html")

def validate():
    if not os.path.exists(INDEX_FILE):
        print(f"[ERRO] Arquivo {INDEX_FILE} não encontrado!")
        sys.exit(1)
        
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        
    size_kb = len(content.encode('utf-8')) / 1024
    lines = len(content.splitlines())
    
    # Verificações de integridade dos componentes essenciais
    checks = {
        "Tag HTML e Head": "<html" in content and "<head" in content,
        "Player Cinematográfico (#playerModal)": 'id="playerModal"' in content,
        "Ficha Técnica de Filmes (#movieDetailsModal)": 'id="movieDetailsModal"' in content,
        "Seletor de Séries (#seriesModal)": 'id="seriesModal"' in content,
        "Modal de Backup (#backupModal)": 'id="backupModal"' in content,
        "Hub do Controle Remoto SSE": "/api/remote/events" in content,
        "Sincronização de Estado": "/api/user_state" in content,
    }
    
    print("=" * 65)
    print("CINELOCAL - VALIDADOR DE INTERFACE WEB (FONTE DA VERDADE)")
    print("=" * 65)
    print(f"Arquivo:   {INDEX_FILE}")
    print(f"Dimensões: {lines:,} linhas • {size_kb:.1f} KB")
    print("-" * 65)
    
    all_ok = True
    for label, passed in checks.items():
        status = "[OK]  " if passed else "[FALHA]"
        print(f"  {status:<8} {label}")
        if not passed:
            all_ok = False
            
    print("=" * 65)
    if all_ok:
        print("Interface web íntegra e pronta para uso!")
    else:
        print("Aviso: Alguns componentes essenciais podem estar ausentes.")
        
    return all_ok

if __name__ == "__main__":
    validate()

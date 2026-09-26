@echo off
chcp 65001 >nul
title CineLocal - Buscar Metadados TMDb
cd /d "%~dp0"

echo ============================================================================
echo       🎬 CINELOCAL - ENRIQUECEDOR AUTOMÁTICO DE METADADOS (TMDB)
echo ============================================================================
echo.
python app\buscar_metadados_tmdb.py

echo.
pause

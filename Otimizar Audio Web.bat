@echo off
title CineLocal - Otimizador de Audio Web
chcp 65001 > nul
cd /d "%~dp0app"

echo =======================================================
echo     CineLocal - Otimizar Audio para Navegador e TV
echo =======================================================
echo.
python otimizar_audio_web.py
echo.
pause

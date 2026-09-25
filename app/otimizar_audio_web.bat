@echo off
title CineLocal - Otimizador de Audio Web
chcp 65001 > nul
cd /d "%~dp0"

echo =======================================================
echo     CineLocal - Otimizar Audio para Navegador e TV
echo =======================================================
echo.
python otimizar_audio_web.py
echo.
echo Processo finalizado!
pause

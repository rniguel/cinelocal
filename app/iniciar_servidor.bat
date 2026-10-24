@echo off
title CineLocal - Servidor de Streaming
chcp 65001 > nul
cd /d "%~dp0"
echo =======================================================
echo   CineLocal - Servidor de Streaming (TV e Celular)
echo =======================================================
echo.
:: Libera a porta 8000 caso tenha ficado presa em segundo plano
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 " ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
)
python servidor.py --no-browser
pause

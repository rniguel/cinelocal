@echo off
title CineLocal - Servidor Local
chcp 65001 > nul
cd /d "%~dp0app"

echo =======================================================
echo          Iniciando CineLocal Home Theater
echo =======================================================
echo.
python servidor.py --browser
pause

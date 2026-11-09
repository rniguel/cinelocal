@echo off
title CineLocal - Compilador de Executavel (.exe)
chcp 65001 > nul
cd /d "%~dp0"

echo =======================================================
echo     CineLocal - Gerador de Executavel Desktop (.exe)
echo =======================================================
echo.
python build_desktop.py
echo.
echo =======================================================
echo Executavel gerado em: dist\CineLocal\CineLocal.exe
echo =======================================================
pause

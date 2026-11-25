@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Instalacja edge-tts...
py -m pip install --upgrade edge-tts
if errorlevel 1 (echo Blad instalacji edge-tts & pause & exit /b 1)
echo Pobieranie gotowych rozdzialow 1-3...
py generator.py download
echo Generowanie kolejnych rozdzialow z dostarczonych tekstow...
py generator.py generate --start 4 --end 73
py generator.py check
echo Po uzyskaniu kompletu uruchom: py generator.py join
pause

@echo off
title Monitor de Consumos de Pacientes
echo Iniciando Sistema de Automatizacion...
cd /d "f:\EDISON\computador\VARIOS EDISON\PROHIBIDO NO TOCAR\CursoPrepHenry\automatizacion_consumos"
call .venv\Scripts\activate
python app.py
pause

@echo off
if not exist "%~dp0.venv" (
  echo init virtual env
  python -m venv .venv
  call %~dp0.venv\Scripts\activate.bat
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  echo please manualy add env vars into %~dp0.venv\Scripts\activate.bat 
)
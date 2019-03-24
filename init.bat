@echo off
if not exist "%~dp0.venv" (
  echo switch to develop branch...
  git checkout develop
  echo init virtual env...
  python -m venv .venv
  call %~dp0.venv\Scripts\activate.bat
  echo upgrade pip...
  python -m pip install --upgrade pip
  echo install requirements
  pip install -r requirements.txt
  echo !!! please manualy add env vars into %~dp0.venv\Scripts\activate.bat !!! 
)
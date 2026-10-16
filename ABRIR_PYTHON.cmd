@echo off
setlocal
title StreamView - Dashboard Python
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" iniciar_dashboard.py
  goto fin
)
py -3 -c "import sys; assert sys.version_info >= (3,11)" >nul 2>&1
if not errorlevel 1 (
  py -3 iniciar_dashboard.py
  goto fin
)
python -c "import sys; assert sys.version_info >= (3,11)" >nul 2>&1
if not errorlevel 1 (
  python iniciar_dashboard.py
  goto fin
)
set "SV_RUNTIME=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%SV_RUNTIME%" (
  "%SV_RUNTIME%" iniciar_dashboard.py
  goto fin
)
echo No se encontro Python 3.11 o superior.
echo Instale Python desde https://www.python.org/downloads/windows/
echo Active la opcion Add Python to PATH durante la instalacion.
:fin
pause

@echo off
setlocal
cd /d "%~dp0"
set "TASK_PYTHON=%~dp0.venv\Scripts\python.exe"
if not exist "%TASK_PYTHON%" set "TASK_PYTHON=%USERPROFILE%\seminario-build\python\python.exe"
if not exist "%TASK_PYTHON%" (
  echo Instale Python 3.12 e siga os comandos de instalacao do README.
  echo Crie .venv e instale requirements.txt antes de iniciar.
  pause
  exit /b 1
)
echo Abra http://127.0.0.1:8501 no navegador.
echo Mantenha esta janela aberta. Ctrl+C encerra a aplicacao.
"%TASK_PYTHON%" -X utf8 -c "import runpy,sys;sys.path.insert(0,'src');runpy.run_path('src/app.py',run_name='__main__')"
pause

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) {
    throw 'Instale Python 3.12 e execute: python -m venv .venv; .venv\Scripts\python.exe -m pip install -r requirements.txt'
}
Write-Host 'Abra http://127.0.0.1:8501 no navegador. Ctrl+C encerra o servidor.'
& $taskPython -X utf8 src/app.py

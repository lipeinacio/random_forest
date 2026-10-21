$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Instale Python 3.12 ou superior e tente novamente.' }
}
& '.venv/Scripts/python.exe' -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar dependencias.' }
& '.venv/Scripts/python.exe' src/baixar_dados.py
if ($LASTEXITCODE -ne 0) { throw 'Falha ao obter/verificar o dataset.' }
& '.venv/Scripts/python.exe' src/pipeline.py
if ($LASTEXITCODE -ne 0) { throw 'Falha na execucao do pipeline.' }
& '.venv/Scripts/python.exe' src/prever.py
if ($LASTEXITCODE -ne 0) { throw 'Falha na demonstracao de predicao.' }

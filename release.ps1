param(
    [switch]$IncludeAppImports = $false
)

$ErrorActionPreference = 'Stop'

function Write-Step($message) {
    Write-Host "`n==> $message" -ForegroundColor Cyan
}

function Invoke-PythonSnippet {
    param(
        [string]$Code
    )
    & $pythonExe -c $Code
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code $LASTEXITCODE"
    }
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $scriptRoot))
$pythonExe = Join-Path $workspaceRoot ".venv\Scripts\python.exe"
$robutilsRoot = Join-Path $scriptRoot "robutils"
$rJournalerRoot = Split-Path -Parent $scriptRoot

if (-not (Test-Path $pythonExe)) {
    throw "Python interpreter not found at $pythonExe"
}

Write-Step "Using Python interpreter"
& $pythonExe --version

Write-Step "Reading robutils version"
$versionCode = @"
import sys
sys.path.insert(0, r'$scriptRoot')
import robutils
print(robutils.__version__)
"@
Invoke-PythonSnippet -Code $versionCode

Write-Step "Running robutils import smoke test"
$importCode = @"
import importlib
import sys
import pathlib
sys.path.insert(0, r'$scriptRoot')
modules = ['robutils', 'robutils.text', 'robutils.math', 'robutils.tools', 'robutils.containers']
for m in modules:
    importlib.import_module(m)
    print('OK', m)
"@
Invoke-PythonSnippet -Code $importCode

if ($IncludeAppImports) {
    Write-Step "Running rJournaler import smoke test"
    $appImportCode = @"
import os
import sys
sys.path.insert(0, r'$scriptRoot')
os.chdir(r'$rJournalerRoot')
import core.config
import core.stats_collector
import rJournalEditor
print('OK rJournaler imports')
"@
    Invoke-PythonSnippet -Code $appImportCode
}

Write-Step "Compiling robutils package"
$compileCode = @"
import py_compile
from pathlib import Path
root = Path(r'$robutilsRoot')
files = sorted(root.rglob('*.py'))
for f in files:
    py_compile.compile(str(f), doraise=True)
print(f'Compiled {len(files)} files')
"@
Invoke-PythonSnippet -Code $compileCode

Write-Step "Release validation complete"
Write-Host "All checks passed." -ForegroundColor Green

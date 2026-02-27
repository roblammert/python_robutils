param(
    [switch]$CheckDocsSync = $true,
    [switch]$FailOnDocsSync = $false
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
$readmeFile = Join-Path $scriptRoot "README.md"
$changelogFile = Join-Path $scriptRoot "CHANGELOG.md"

if (-not (Test-Path $pythonExe)) {
    throw "Python interpreter not found at $pythonExe"
}

Write-Step "Checking required documentation files"
if (-not (Test-Path $readmeFile)) {
    throw "Missing documentation file: $readmeFile"
}
if (-not (Test-Path $changelogFile)) {
    throw "Missing documentation file: $changelogFile"
}
Write-Host "Found README.md and CHANGELOG.md"

if ($CheckDocsSync) {
    Write-Step "Checking documentation sync against git changes"
    $gitCommand = Get-Command git -ErrorAction SilentlyContinue
    if (-not $gitCommand) {
        Write-Host "Git not found; skipping docs sync check." -ForegroundColor Yellow
    }
    else {
        $insideWorkTree = cmd /c "git -C \"$workspaceRoot\" rev-parse --is-inside-work-tree 2>nul"
        if ($LASTEXITCODE -ne 0 -or $insideWorkTree.Trim() -ne 'true') {
            Write-Host "Workspace is not a git work tree; skipping docs sync check." -ForegroundColor Yellow
        }
        else {
            $changedPaths = @(
                (cmd /c "git -C \"$workspaceRoot\" diff --name-only 2>nul")
                (cmd /c "git -C \"$workspaceRoot\" diff --name-only --cached 2>nul")
                (cmd /c "git -C \"$workspaceRoot\" ls-files --others --exclude-standard 2>nul")
            ) | Where-Object { $_ -and $_.Trim().Length -gt 0 } | ForEach-Object { $_.Trim() } | Sort-Object -Unique

            if ($changedPaths.Count -eq 0) {
                Write-Host "No changed files detected; docs sync check passed." -ForegroundColor Green
            }
            else {
                $docsFiles = @(
                    'README.md',
                    'CHANGELOG.md'
                )

                $codeFiles = $changedPaths | Where-Object {
                    ($_ -like 'robutils/*.py') -or
                    ($_ -like 'robutils/**/*.py') -or
                    ($_ -like '*.ps1')
                }
                $docsTouched = $changedPaths | Where-Object { $docsFiles -contains $_ }

                if ($codeFiles.Count -gt 0 -and $docsTouched.Count -eq 0) {
                    $message = "Code changes detected without docs updates (README.md/CHANGELOG.md)."
                    if ($FailOnDocsSync) {
                        throw $message
                    }
                    Write-Host $message -ForegroundColor Yellow
                }
                else {
                    Write-Host "Docs sync check passed." -ForegroundColor Green
                }
            }
        }
    }
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
Write-Host "Reminder: confirm README.md and CHANGELOG.md are updated for this change." -ForegroundColor Yellow

# Maintainer sweep — run all executable specimen tests from repo root.
# Usage: .\verify_examples.ps1

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$fail = 0

function Step {
    param([string]$Name, [scriptblock]$Action)
    Write-Host ""
    Write-Host "== $Name ==" -ForegroundColor Cyan
    try {
        & $Action
        if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
            throw "exit $LASTEXITCODE"
        }
        Write-Host "OK: $Name" -ForegroundColor Green
    }
    catch {
        Write-Host "FAIL: $Name" -ForegroundColor Red
        Write-Host $_.Exception.Message
        $script:fail = 1
    }
}

Step "Fall tests" {
    Push-Location (Join-Path $root "EXAMPLEmarbles\fall")
    python -m unittest discover -s tests -p "test_*.py" -q
    Pop-Location
}

Step "Lighthouse tests" {
    Push-Location (Join-Path $root "EXAMPLEmarbles\lighthouse")
    python -m unittest discover -s tests -p "test_*.py" -q
    Pop-Location
}

Step "Trench gate suite" {
    Push-Location (Join-Path $root "EXAMPLEmarbles\trench\tests")
    node run-all.mjs
    Pop-Location
}

Step "Cabin hostile floor" {
    Push-Location (Join-Path $root "EXAMPLEmarbles\cabin")
    python tests/test_hostile.py
    Pop-Location
}

if ($fail -ne 0) {
    Write-Host ""
    Write-Host "One or more specimen suites failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "All specimen suites passed." -ForegroundColor Green
exit 0

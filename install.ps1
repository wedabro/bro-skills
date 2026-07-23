# bro-skills Installer for Windows (PowerShell)
# Usage (PowerShell / irm):
#   irm https://raw.githubusercontent.com/wedabro/bro-skills/main/install.ps1 | iex
# Usage (curl in PowerShell / CMD):
#   curl.exe -fsSL https://raw.githubusercontent.com/wedabro/bro-skills/main/install.ps1 -o install.ps1; powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"

Write-Host "⚡ Installing bro-skills..." -ForegroundColor Cyan

# 1. Detect Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Host "❌ Python is required but not found in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.9+ from https://www.python.org/downloads/ and check 'Add Python to PATH'." -ForegroundColor Yellow
    exit 1
}

$pythonExe = $pythonCmd.Source
$pyVersionStr = & $pythonExe --version 2>&1
Write-Host "✔ Found $pyVersionStr" -ForegroundColor Green

# 2. Check Python Version (>= 3.9)
$versionCheck = & $pythonExe -c "import sys; print(1 if sys.version_info >= (3, 9) else 0)"
if ($versionCheck.Trim() -ne "1") {
    Write-Host "❌ Python 3.9 or higher is required." -ForegroundColor Red
    exit 1
}

# 3. Install via pip
Write-Host "📦 Installing bro-skills via pip..." -ForegroundColor Yellow
& $pythonExe -m pip install --upgrade git+https://github.com/wedabro/bro-skills.git

# 4. Verify Installation
$broSkillsCmd = Get-Command bro-skills -ErrorAction SilentlyContinue
if ($broSkillsCmd) {
    Write-Host "`n🎉 bro-skills installed successfully!" -ForegroundColor Green
    & bro-skills version
} else {
    Write-Host "`n⚠️ bro-skills was installed, but the 'bro-skills' command is not in your current PATH." -ForegroundColor Yellow
    Write-Host "Please restart your terminal or ensure Python Scripts folder is in your environment PATH." -ForegroundColor Yellow
}

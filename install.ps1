# bro-skills installer for Windows
# Usage: irm https://raw.githubusercontent.com/wedabro/bro-skills/main/install.ps1 | iex

$ErrorActionPreference = "Stop"
$repo = "wedabro/bro-skills"
$installDir = Join-Path $env:LOCALAPPDATA "Programs\bro-skills"
$destination = Join-Path $installDir "bro-skills.cmd"
$srcDir = Join-Path $env:LOCALAPPDATA "bro-skills-src"

$pyCmd = Get-Command python, python3, py -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $pyCmd) {
    throw "Python 3 is required to install bro-skills. Please install Python 3 and try again."
}

Write-Host "⚡ Installing latest bro-skills from GitHub main branch..." -ForegroundColor Cyan

# 1. Try pip install first if pip is available
$hasPip = $false
try {
    & $pyCmd.Name -m pip --version *>$null
    if ($LASTEXITCODE -eq 0) { $hasPip = $true }
} catch {}

if ($hasPip) {
    try {
        & $pyCmd.Name -m pip install --no-cache-dir --force-reinstall --upgrade "git+https://github.com/$repo.git@main"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ bro-skills installed successfully via pip!" -ForegroundColor Green
            & bro-skills version
            exit 0
        }
    } catch {}
}

# 2. Fallback: Use Python stdlib to download and extract main.zip
$pyScript = @"
import urllib.request, zipfile, io, os, shutil, time
ts = int(time.time())
url = f'https://github.com/$repo/archive/refs/heads/main.zip?t={ts}'
headers = {'User-Agent': 'bro-skills-installer', 'Cache-Control': 'no-cache'}

print('Downloading latest source archive...')
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = resp.read()

tmp_extract = os.path.expanduser('~/.bro-skills-tmp')
if os.path.exists(tmp_extract):
    shutil.rmtree(tmp_extract)

print('Extracting package contents...')
with zipfile.ZipFile(io.BytesIO(data)) as zf:
    zf.extractall(tmp_extract)

src_folder = os.path.join(tmp_extract, 'bro-skills-main')
dest_folder = r'$srcDir'

if os.path.exists(dest_folder):
    shutil.rmtree(dest_folder)

shutil.copytree(src_folder, dest_folder)
shutil.rmtree(tmp_extract, ignore_errors=True)
print('Source files installed successfully.')
"@

& $pyCmd.Name -c $pyScript

New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Set-Content -Path $destination -Value "@echo off`r`n`"$($pyCmd.Source)`" `"$srcDir\ssd.py`" %*" -Encoding ASCII

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$pathEntries = @($userPath -split ";" | Where-Object { $_ })
if ($pathEntries -notcontains $installDir) {
    $newPath = (($pathEntries + $installDir) -join ";")
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
}

Write-Host "✅ bro-skills installed successfully at $destination!" -ForegroundColor Green
& $destination version

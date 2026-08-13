# bro-skills installer for Windows
# Usage: irm https://raw.githubusercontent.com/wedabro/bro-skills/main/install.ps1 | iex

$ErrorActionPreference = "Stop"
$repo = "wedabro/bro-skills"
$asset = "bro-skills-windows-x86_64.exe"
$installDir = Join-Path $env:LOCALAPPDATA "Programs\bro-skills"
$destination = Join-Path $installDir "bro-skills.exe"
$baseUrl = "https://github.com/$repo/releases/latest/download"
$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("bro-skills-" + [guid]::NewGuid())

# 1. Prefer Python / Pip installation if available to get the latest main release
$pyCmd = Get-Command python, python3, py -ErrorAction SilentlyContinue | Select-Object -First 1
if ($pyCmd) {
    $ts = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    # Check if pip is available
    $hasPip = $false
    try {
        & $pyCmd.Name -m pip --version *>$null
        if ($LASTEXITCODE -eq 0) { $hasPip = $true }
    } catch {}

    if ($hasPip) {
        Write-Host "⚡ Installing latest bro-skills via Python ($($pyCmd.Name))..." -ForegroundColor Cyan
        try {
            & $pyCmd.Name -m pip install --no-cache-dir --force-reinstall --upgrade "git+https://github.com/$repo.git@main"
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ bro-skills installed successfully!" -ForegroundColor Green
                & bro-skills version
                exit 0
            }
        } catch {
            try {
                & $pyCmd.Name -m pip install --no-cache-dir --force-reinstall --upgrade "https://github.com/$repo/archive/refs/heads/main.zip?t=$ts"
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ bro-skills installed successfully via fallback archive!" -ForegroundColor Green
                    & bro-skills version
                    exit 0
                }
            } catch {}
        }
    }

    # Python is available without pip: Download main.zip and create source wrapper
    Write-Host "⚡ Installing latest bro-skills via $($pyCmd.Name) source runner..." -ForegroundColor Cyan
    $srcDir = Join-Path $env:LOCALAPPDATA "bro-skills-src"
    $zipPath = Join-Path $tempDir "main.zip"
    Invoke-WebRequest "https://github.com/$repo/archive/refs/heads/main.zip?t=$ts" -OutFile $zipPath -UseBasicParsing

    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
    & $pyCmd.Name -c "import zipfile; zipfile.ZipFile(r'$zipPath').extractall(r'$tempDir')"
    
    if (Test-Path $srcDir) { Remove-Item -LiteralPath $srcDir -Recurse -Force }
    New-Item -ItemType Directory -Force -Path $srcDir | Out-Null
    Copy-Item -Path (Join-Path $tempDir "bro-skills-main\*") -Destination $srcDir -Recurse -Force

    $cmdWrapper = Join-Path $installDir "bro-skills.cmd"
    New-Item -ItemType Directory -Force -Path $installDir | Out-Null
    Set-Content -Path $cmdWrapper -Value "@echo off`r`n`"$($pyCmd.Source)`" `"$srcDir\ssd.py`" %*" -Encoding ASCII

    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $pathEntries = @($userPath -split ";" | Where-Object { $_ })
    if ($pathEntries -notcontains $installDir) {
        $newPath = (($pathEntries + $installDir) -join ";")
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    }

    Write-Host "✅ bro-skills installed successfully at $cmdWrapper!" -ForegroundColor Green
    & $cmdWrapper version
    exit 0
}

# 2. Fallback to standalone binary download
$architecture = $env:PROCESSOR_ARCHITEW6432
if (-not $architecture) {
    $architecture = $env:PROCESSOR_ARCHITECTURE
}
if ($architecture -notin @("AMD64", "x86_64")) {
    throw "bro-skills currently provides a standalone Windows binary for x64 only (detected: $architecture)."
}

Write-Host "Installing bro-skills standalone binary..." -ForegroundColor Cyan

try {
    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
    New-Item -ItemType Directory -Force -Path $installDir | Out-Null

    $download = Join-Path $tempDir $asset
    $checksumFile = "$download.sha256"
    Invoke-WebRequest "$baseUrl/$asset" -OutFile $download -UseBasicParsing
    Invoke-WebRequest "$baseUrl/$asset.sha256" -OutFile $checksumFile -UseBasicParsing

    $expected = ((Get-Content -Raw $checksumFile).Trim() -split "\s+")[0].ToLowerInvariant()
    $actual = (Get-FileHash $download -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $expected) {
        throw "SHA-256 verification failed. Expected $expected but downloaded $actual."
    }

    Move-Item -Force $download $destination

    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $pathEntries = @($userPath -split ";" | Where-Object { $_ })
    if ($pathEntries -notcontains $installDir) {
        $newPath = (($pathEntries + $installDir) -join ";")
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "Added $installDir to your user PATH." -ForegroundColor Yellow
    }
    if (($env:Path -split ";") -notcontains $installDir) {
        $env:Path = "$env:Path;$installDir"
    }

    Write-Host "bro-skills installed successfully." -ForegroundColor Green
    & $destination version
    if ($LASTEXITCODE -ne 0) {
        Remove-Item -LiteralPath $destination -Force
        throw "The downloaded bro-skills executable could not run; installation was rolled back."
    }
    Write-Host "Open a new terminal, then run: bro-skills" -ForegroundColor Cyan
}
finally {
    if (Test-Path $tempDir) {
        Remove-Item -LiteralPath $tempDir -Recurse -Force
    }
}


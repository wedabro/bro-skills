# bro-skills standalone installer for Windows x64
# Usage: irm https://raw.githubusercontent.com/wedabro/bro-skills/main/install.ps1 | iex

$ErrorActionPreference = "Stop"
$repo = "wedabro/bro-skills"
$asset = "bro-skills-windows-x86_64.exe"
$installDir = Join-Path $env:LOCALAPPDATA "Programs\bro-skills"
$destination = Join-Path $installDir "bro-skills.exe"
$baseUrl = "https://github.com/$repo/releases/latest/download"
$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("bro-skills-" + [guid]::NewGuid())

$architecture = $env:PROCESSOR_ARCHITEW6432
if (-not $architecture) {
    $architecture = $env:PROCESSOR_ARCHITECTURE
}
if ($architecture -notin @("AMD64", "x86_64")) {
    throw "bro-skills currently provides a standalone Windows binary for x64 only (detected: $architecture)."
}

Write-Host "Installing bro-skills standalone..." -ForegroundColor Cyan

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

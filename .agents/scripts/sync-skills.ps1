# Sync skills tu .agent sang .kiro voi retry (tranh file lock khi Kiro dang index)
param([string[]]$Skills)
if (-not $Skills) {
    $Skills = Get-ChildItem "$PSScriptRoot\..\skills" -Directory | Select-Object -ExpandProperty Name
}
$root = Resolve-Path "$PSScriptRoot\.."
$agentRoot = Join-Path $root 'skills'
$kiroRoot = Join-Path (Resolve-Path "$root\..") '.kiro\skills'
$fail = 0
foreach ($s in $Skills) {
    $src = Join-Path $agentRoot "$s\SKILL.md"
    $dst = Join-Path $kiroRoot "$s\SKILL.md"
    if (-not (Test-Path $src)) { Write-Host "SKIP (no src): $s"; continue }
    $ok = $false
    for ($i = 0; $i -lt 5 -and -not $ok; $i++) {
        try {
            $content = Get-Content $src -Raw
            New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
            [System.IO.File]::WriteAllText($dst, $content)
            $ok = $true
        } catch {
            Start-Sleep -Milliseconds 400
        }
    }
    if (-not $ok) { Write-Host "FAIL: $s"; $fail++ }
}
if ($fail -eq 0) { Write-Host "Sync OK: $($Skills.Count) skills" } else { Write-Host "Sync FAILED: $fail" }

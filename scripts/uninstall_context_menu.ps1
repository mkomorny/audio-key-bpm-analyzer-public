# Uninstall Windows Explorer Context Menu: "Analyze Key, Scale, Pitch & BPM"

$extensions = @(".wav", ".mp3", ".flac", ".m4a", ".aiff", ".aif", ".ogg")

Write-Host "Uninstalling Windows Explorer Context Menu..." -ForegroundColor Cyan

foreach ($ext in $extensions) {
    $regKey = "HKCU:\Software\Classes\SystemFileAssociations\$ext\shell\BasicPitchAnalyze"
    if (Test-Path $regKey) {
        Remove-Item -Path $regKey -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  [-] Removed $ext" -ForegroundColor Yellow
    }
}

$audioRegKey = "HKCU:\Software\Classes\SystemFileAssociations\audio\shell\BasicPitchAnalyze"
if (Test-Path $audioRegKey) {
    Remove-Item -Path $audioRegKey -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  [-] Removed audio association" -ForegroundColor Yellow
}

Write-Host "`n[SUCCESS] Context menu uninstalled." -ForegroundColor Green

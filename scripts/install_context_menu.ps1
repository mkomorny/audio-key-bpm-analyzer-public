# Install Windows Explorer Context Menu: "Analyze Key, Scale, Pitch & BPM"
# Registers under HKCU:\Software\Classes\SystemFileAssociations (no Administrator rights needed)

$scriptPath = "C:\Users\<you>\.agents\skills\audio-key-bpm-analyzer\scripts\analyze_audio.py"
$pythonExe = "C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python.exe"
}

$commandStr = "cmd.exe /c start `"Analyze Key, Scale & BPM`" `"$pythonExe`" `"$scriptPath`" `"%1`" --pause"
$menuTitle = "Analyze Key, Scale, Pitch & BPM (Basic Pitch)"

$extensions = @(".wav", ".mp3", ".flac", ".m4a", ".aiff", ".aif", ".ogg")

Write-Host "Installing Windows Explorer Context Menu: '$menuTitle'..." -ForegroundColor Cyan

foreach ($ext in $extensions) {
    $regKey = "HKCU:\Software\Classes\SystemFileAssociations\$ext\shell\BasicPitchAnalyze"
    $cmdKey = "$regKey\command"

    New-Item -Path $regKey -Force | Out-Null
    Set-ItemProperty -Path $regKey -Name "(Default)" -Value $menuTitle -Force
    Set-ItemProperty -Path $regKey -Name "Icon" -Value "shell32.dll,138" -Force # Music note icon

    New-Item -Path $cmdKey -Force | Out-Null
    Set-ItemProperty -Path $cmdKey -Name "(Default)" -Value $commandStr -Force
    Write-Host "  [+] Registered for $ext" -ForegroundColor Green
}

# Also register for generic audio association
$audioRegKey = "HKCU:\Software\Classes\SystemFileAssociations\audio\shell\BasicPitchAnalyze"
$audioCmdKey = "$audioRegKey\command"
New-Item -Path $audioRegKey -Force | Out-Null
Set-ItemProperty -Path $audioRegKey -Name "(Default)" -Value $menuTitle -Force
Set-ItemProperty -Path $audioRegKey -Name "Icon" -Value "shell32.dll,138" -Force
New-Item -Path $audioCmdKey -Force | Out-Null
Set-ItemProperty -Path $audioCmdKey -Name "(Default)" -Value $commandStr -Force
Write-Host "  [+] Registered for SystemFileAssociations\audio" -ForegroundColor Green

Write-Host "`n[SUCCESS] Context menu installed! Right-click any audio file in Explorer to analyze." -ForegroundColor Yellow

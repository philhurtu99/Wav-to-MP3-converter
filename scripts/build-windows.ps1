$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

python -m pip install -U pip
python -m pip install -e ".[dev]"
pytest -q

Remove-Item -Recurse -Force build, dist, release -ErrorAction SilentlyContinue
pyinstaller --noconfirm packaging/pyinstaller-cli.spec
pyinstaller --noconfirm packaging/pyinstaller-gui.spec

New-Item -ItemType Directory -Force release | Out-Null
Compress-Archive -Path "dist\WAV to MP3 Converter\*" -DestinationPath "release\WAV-to-MP3-Converter-Windows.zip" -Force
Copy-Item "dist\wav-to-mp3.exe" "release\wav-to-mp3-windows.exe" -Force

Write-Host "Artifacts created in release/:"
Get-ChildItem release

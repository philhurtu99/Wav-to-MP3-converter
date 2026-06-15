#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python -m pip install -U pip
python -m pip install -e '.[dev]'
pytest -q

rm -rf build dist
pyinstaller --noconfirm packaging/pyinstaller-cli.spec
pyinstaller --noconfirm packaging/pyinstaller-gui.spec

mkdir -p release
case "$(uname -s)" in
  Darwin)
    ditto -c -k --sequesterRsrc --keepParent "dist/Convertisseur WAV vers MP3.app" "release/Convertisseur-WAV-vers-MP3-macOS.zip"
    cp "dist/wav-to-mp3" "release/wav-to-mp3-macos"
    ;;
  Linux)
    tar -C dist -czf "release/wav-to-mp3-linux.tar.gz" wav-to-mp3
    ;;
  *)
    echo "Plateforme non gérée par ce script bash. Utilise scripts/build-windows.ps1 sur Windows." >&2
    exit 1
    ;;
esac

echo "Artefacts créés dans release/:"
find release -maxdepth 1 -type f -print

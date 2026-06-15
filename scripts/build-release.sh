#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python -m pip install -U pip
python -m pip install -e '.[dev]'
pytest -q

rm -rf build dist release
pyinstaller --noconfirm packaging/pyinstaller-cli.spec
pyinstaller --noconfirm packaging/pyinstaller-gui.spec

mkdir -p release
case "$(uname -s)" in
  Darwin)
    ditto -c -k --sequesterRsrc --keepParent "dist/WAV to MP3 Converter.app" "release/WAV-to-MP3-Converter-macOS.zip"
    cp "dist/wav-to-mp3" "release/wav-to-mp3-macos"
    ;;
  Linux)
    tar -C dist -czf "release/wav-to-mp3-linux.tar.gz" wav-to-mp3
    ;;
  *)
    echo "Unsupported platform for this bash script. Use scripts/build-windows.ps1 on Windows." >&2
    exit 1
    ;;
esac

echo "Artifacts created in release/:"
find release -maxdepth 1 -type f -print

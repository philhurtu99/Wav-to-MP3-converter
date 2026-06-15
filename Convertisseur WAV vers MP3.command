#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv
  . .venv/bin/activate
  pip install -U pip
  pip install -e .
else
  . .venv/bin/activate
fi
python -m wav_to_mp3.gui

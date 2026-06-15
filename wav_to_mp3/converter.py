from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class ConversionError(Exception):
    """Erreur affichable à l'utilisateur pendant une conversion."""


FFMPEG_CANDIDATES = [
    "ffmpeg",
    "/opt/homebrew/bin/ffmpeg",  # Homebrew Apple Silicon
    "/usr/local/bin/ffmpeg",  # Homebrew Intel
    "/opt/local/bin/ffmpeg",  # MacPorts
    "/usr/bin/ffmpeg",
]


def find_ffmpeg() -> Path | None:
    """Trouve ffmpeg même quand l'app macOS est lancée depuis Finder avec un PATH minimal."""
    for candidate in FFMPEG_CANDIDATES:
        if "/" not in candidate:
            resolved = shutil.which(candidate)
            if resolved:
                return Path(resolved)
            continue

        path = Path(candidate)
        if path.exists() and path.is_file():
            return path

    return None


def output_path_for(source: Path, output_dir: str | Path | None = None) -> Path:
    if output_dir is None:
        return source.with_suffix(".mp3")

    return Path(output_dir).expanduser().resolve() / source.with_suffix(".mp3").name


def convert_wav_to_mp3(source: str | Path, bitrate: str = "320k", output_dir: str | Path | None = None) -> Path:
    source = Path(source).expanduser().resolve()

    if source.suffix.lower() != ".wav":
        raise ConversionError(f"{source.name} n'est pas un fichier WAV.")

    if not source.exists():
        raise ConversionError(f"Fichier introuvable: {source}")

    ffmpeg = find_ffmpeg()
    if ffmpeg is None:
        raise ConversionError("ffmpeg n'est pas installé. Installe-le avec: brew install ffmpeg")

    destination = output_path_for(source, output_dir)
    destination.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(ffmpeg),
        "-y",
        "-i",
        str(source),
        "-codec:a",
        "libmp3lame",
        "-b:a",
        bitrate,
        str(destination),
    ]

    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "erreur inconnue"
        raise ConversionError(f"Conversion impossible pour {source.name}: {detail}")

    return destination

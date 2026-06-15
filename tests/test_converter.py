import os
from pathlib import Path
import subprocess

import pytest

from wav_to_mp3.converter import ConversionError, convert_wav_to_mp3, find_ffmpeg, output_path_for


def test_output_path_for_replaces_wav_extension_with_mp3(tmp_path):
    wav = tmp_path / "Ma chanson.WAV"

    result = output_path_for(wav)

    assert result == tmp_path / "Ma chanson.mp3"


def test_output_path_for_uses_selected_output_directory(tmp_path):
    source_dir = tmp_path / "source"
    output_dir = tmp_path / "exports mp3"
    source_dir.mkdir()
    output_dir.mkdir()
    wav = source_dir / "Ma chanson.WAV"

    result = output_path_for(wav, output_dir)

    assert result == output_dir / "Ma chanson.mp3"


def test_find_ffmpeg_checks_homebrew_path_when_finder_path_is_minimal(monkeypatch):
    monkeypatch.setenv("PATH", "/usr/bin:/bin:/usr/sbin:/sbin")

    result = find_ffmpeg()

    assert result is not None
    assert result.name == "ffmpeg"
    assert result.exists()


def test_convert_wav_to_mp3_rejects_non_wav_file(tmp_path):
    source = tmp_path / "track.aiff"
    source.write_bytes(b"not a wav")

    with pytest.raises(ConversionError, match="WAV file"):
        convert_wav_to_mp3(source)


def test_convert_wav_to_mp3_creates_playable_mp3_even_with_finder_like_path(tmp_path, monkeypatch):
    wav = tmp_path / "tone.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=440:duration=0.25",
            str(wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    monkeypatch.setenv("PATH", "/usr/bin:/bin:/usr/sbin:/sbin")

    output_dir = tmp_path / "converted"
    mp3 = convert_wav_to_mp3(wav, output_dir=output_dir)

    assert mp3 == output_dir / "tone.mp3"
    assert not (tmp_path / "tone.mp3").exists()
    assert mp3.exists()
    assert mp3.stat().st_size > 0

    ffprobe = Path(os.environ.get("FFPROBE", "/opt/homebrew/bin/ffprobe"))
    if not ffprobe.exists():
        ffprobe = Path("ffprobe")
    probe = subprocess.run(
        [str(ffprobe), "-v", "error", "-show_entries", "format=format_name", "-of", "default=nw=1:nk=1", str(mp3)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "mp3" in probe.stdout

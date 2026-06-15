from __future__ import annotations

import subprocess
from pathlib import Path

from wav_to_mp3 import cli


def make_wav(path: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=330:duration=0.15",
            str(path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def test_cli_converts_multiple_wavs_to_selected_output_dir(tmp_path, capsys):
    source_dir = tmp_path / "sources"
    output_dir = tmp_path / "mp3"
    source_dir.mkdir()
    wav_a = source_dir / "a.wav"
    wav_b = source_dir / "b.wav"
    make_wav(wav_a)
    make_wav(wav_b)

    exit_code = cli.main([str(wav_a), str(wav_b), "--output-dir", str(output_dir)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert (output_dir / "a.mp3").exists()
    assert (output_dir / "b.mp3").exists()
    assert "2 fichier(s) converti(s)" in captured.out


def test_cli_accepts_directory_input_and_converts_wavs(tmp_path):
    input_dir = tmp_path / "album"
    output_dir = tmp_path / "exports"
    input_dir.mkdir()
    make_wav(input_dir / "track1.wav")
    make_wav(input_dir / "track2.WAV")
    (input_dir / "ignore.txt").write_text("not audio")

    exit_code = cli.main([str(input_dir), "--output-dir", str(output_dir)])

    assert exit_code == 0
    assert sorted(path.name for path in output_dir.glob("*.mp3")) == ["track1.mp3", "track2.mp3"]


def test_cli_returns_error_for_missing_inputs(capsys):
    exit_code = cli.main([])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Au moins un fichier ou dossier" in captured.err

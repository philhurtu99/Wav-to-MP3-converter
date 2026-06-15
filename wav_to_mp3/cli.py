from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .converter import ConversionError, convert_wav_to_mp3


def collect_wav_files(inputs: list[str]) -> list[Path]:
    wav_files: list[Path] = []
    for raw_input in inputs:
        path = Path(raw_input).expanduser()
        if path.is_dir():
            wav_files.extend(sorted(child for child in path.iterdir() if child.is_file() and child.suffix.lower() == ".wav"))
        elif path.is_file() and path.suffix.lower() == ".wav":
            wav_files.append(path)
        elif path.exists():
            print(f"Ignored, not a WAV file: {path}", file=sys.stderr)
        else:
            print(f"Not found: {path}", file=sys.stderr)
    return wav_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wav-to-mp3",
        description="Convert WAV files to MP3. Accepts files or folders.",
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help=".wav files or folders containing .wav files",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Output folder. Default: same folder as each WAV file.",
    )
    parser.add_argument(
        "-b",
        "--bitrate",
        default="320k",
        help="MP3 bitrate passed to ffmpeg, e.g. 192k, 256k, 320k. Default: 320k.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.inputs:
        print("At least one WAV file or folder is required.", file=sys.stderr)
        parser.print_usage(sys.stderr)
        return 2

    wav_files = collect_wav_files(args.inputs)
    if not wav_files:
        print("No valid WAV files found.", file=sys.stderr)
        return 1

    successes: list[Path] = []
    failures: list[str] = []

    for wav_file in wav_files:
        try:
            mp3 = convert_wav_to_mp3(wav_file, bitrate=args.bitrate, output_dir=args.output_dir)
            successes.append(mp3)
            print(f"OK: {wav_file} -> {mp3}")
        except ConversionError as error:
            failures.append(str(error))
            print(f"ERROR: {error}", file=sys.stderr)

    print(f"{len(successes)} file(s) converted.")
    if failures:
        print(f"{len(failures)} error(s).", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

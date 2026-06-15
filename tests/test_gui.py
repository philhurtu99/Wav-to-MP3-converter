from pathlib import Path

from wav_to_mp3.gui import parse_dropped_paths


def test_parse_dropped_paths_handles_macos_paths_with_spaces():
    raw = "{/Users/phil/Music/Ma chanson.wav} /Users/phil/Music/simple.wav"

    result = parse_dropped_paths(raw)

    assert result == [
        Path("/Users/phil/Music/Ma chanson.wav"),
        Path("/Users/phil/Music/simple.wav"),
    ]

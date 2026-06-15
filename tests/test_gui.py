from pathlib import Path

from wav_to_mp3.gui import APP_NAME, MainWindow, parse_dropped_paths


def test_parse_dropped_paths_handles_macos_paths_with_spaces():
    raw = "{/Users/phil/Music/My song.wav} /Users/phil/Music/simple.wav"

    result = parse_dropped_paths(raw)

    assert result == [
        Path("/Users/phil/Music/My song.wav"),
        Path("/Users/phil/Music/simple.wav"),
    ]


def test_main_window_uses_english_labels(qapp):
    window = MainWindow()

    assert window.windowTitle() == APP_NAME
    assert "Output: same folder as WAV files" == window.output_label.text()
    assert "Ready." == window.status.text()

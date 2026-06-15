from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from .converter import ConversionError, convert_wav_to_mp3


APP_NAME = "WAV to MP3 Converter"


def parse_dropped_paths(raw: str) -> list[Path]:
    """Parse Tk-style dropped paths, including paths wrapped in braces."""
    paths: list[str] = []
    current: list[str] = []
    in_braces = False

    for char in raw.strip():
        if char == "{" and not in_braces:
            in_braces = True
            current = []
        elif char == "}" and in_braces:
            in_braces = False
            paths.append("".join(current))
            current = []
        elif char == " " and not in_braces:
            if current:
                paths.append("".join(current))
                current = []
        else:
            current.append(char)

    if current:
        paths.append("".join(current))

    return [Path(path) for path in paths if path]


class ConversionWorker(QThread):
    finished = Signal(str, str)

    def __init__(self, files: list[Path], ignored: int = 0, output_dir: Path | None = None) -> None:
        super().__init__()
        self.files = files
        self.ignored = ignored
        self.output_dir = output_dir

    def run(self) -> None:
        successes: list[str] = []
        failures: list[str] = []

        for file in self.files:
            try:
                destination = convert_wav_to_mp3(file, output_dir=self.output_dir)
                successes.append(destination.name)
            except ConversionError as error:
                failures.append(str(error))

        summary_parts = []
        if successes:
            summary_parts.append(f"Success: {len(successes)} MP3 file(s) created: " + ", ".join(successes))
        if self.ignored:
            summary_parts.append(f"Note: {self.ignored} file(s) ignored because they were not WAV files.")
        if failures:
            summary_parts.append("Errors:\n" + "\n".join(failures))

        message = "\n\n".join(summary_parts) if summary_parts else "Nothing to convert."
        level = "error" if failures and not successes else "info"
        self.finished.emit(level, message)


class DropZone(QFrame):
    files_dropped = Signal(list)

    def __init__(self) -> None:
        super().__init__()
        self.setAcceptDrops(True)
        self.setObjectName("dropZone")
        self.setMinimumHeight(220)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Drop your WAV files here\n\nor use the button below")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("dropLabel")
        layout.addWidget(label)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragging", True)
            self.style().unpolish(self)
            self.style().polish(self)
        else:
            event.ignore()

    def dragLeaveEvent(self, event) -> None:  # noqa: ANN001
        self.setProperty("dragging", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        self.setProperty("dragging", False)
        self.style().unpolish(self)
        self.style().polish(self)
        paths = [Path(url.toLocalFile()) for url in event.mimeData().urls() if url.isLocalFile()]
        self.files_dropped.emit(paths)
        event.acceptProposedAction()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.worker: ConversionWorker | None = None
        self.output_dir: Path | None = None
        self.setWindowTitle(APP_NAME)
        self.resize(660, 450)
        self.setMinimumSize(560, 380)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 24, 28, 18)
        layout.setSpacing(14)

        title = QLabel(APP_NAME)
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Drag and drop .wav files here. Choose an output folder if you do not want MP3s next to the WAV files.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        output_row = QHBoxLayout()
        layout.addLayout(output_row)

        output_button = QPushButton("Choose output folder")
        output_button.clicked.connect(self.choose_output_dir)
        output_button.setObjectName("secondaryButton")
        output_row.addWidget(output_button)

        self.output_label = QLabel("Output: same folder as WAV files")
        self.output_label.setObjectName("outputLabel")
        self.output_label.setWordWrap(True)
        output_row.addWidget(self.output_label, stretch=1)

        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self.start_conversion)
        layout.addWidget(self.drop_zone, stretch=1)

        self.progress = QProgressBar()
        self.progress.setRange(0, 1)
        self.progress.setValue(0)
        self.progress.hide()
        layout.addWidget(self.progress)

        bottom = QHBoxLayout()
        layout.addLayout(bottom)

        choose_button = QPushButton("Choose WAV files")
        choose_button.clicked.connect(self.choose_files)
        choose_button.setObjectName("primaryButton")
        bottom.addWidget(choose_button)

        self.status = QLabel("Ready.")
        self.status.setObjectName("status")
        bottom.addWidget(self.status, stretch=1)

        self.setStyleSheet(
            """
            QMainWindow, QWidget { background: #111827; color: #f9fafb; font-family: 'Helvetica Neue'; }
            QLabel#title { font-size: 28px; font-weight: 700; color: #f9fafb; }
            QLabel#subtitle { font-size: 14px; color: #d1d5db; }
            QLabel#status { color: #9ca3af; padding-left: 12px; }
            QLabel#outputLabel { color: #d1d5db; font-size: 13px; }
            QFrame#dropZone { background: #1f2937; border: 2px dashed #60a5fa; border-radius: 18px; }
            QFrame#dropZone[dragging="true"] { background: #172554; border-color: #93c5fd; }
            QLabel#dropLabel { font-size: 22px; font-weight: 700; color: #e5e7eb; }
            QPushButton#primaryButton { background: #2563eb; color: white; border: 0; border-radius: 10px; padding: 11px 18px; font-size: 14px; font-weight: 700; }
            QPushButton#primaryButton:hover { background: #1d4ed8; }
            QPushButton#secondaryButton { background: #374151; color: white; border: 1px solid #4b5563; border-radius: 10px; padding: 9px 14px; font-size: 13px; font-weight: 700; }
            QPushButton#secondaryButton:hover { background: #4b5563; }
            QProgressBar { border: 0; border-radius: 5px; background: #374151; height: 10px; }
            QProgressBar::chunk { background: #60a5fa; border-radius: 5px; }
            """
        )

    def choose_output_dir(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "Choose MP3 output folder",
            str(self.output_dir or Path.home()),
        )
        if not directory:
            return

        self.output_dir = Path(directory)
        self.output_label.setText(f"Output: {self.output_dir}")

    def choose_files(self) -> None:
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Choose WAV files",
            str(Path.home()),
            "WAV files (*.wav);;All files (*)",
        )
        self.start_conversion([Path(name) for name in filenames])

    def start_conversion(self, files: list[Path]) -> None:
        wav_files = [path for path in files if path.suffix.lower() == ".wav"]
        ignored = len(files) - len(wav_files)

        if not wav_files:
            QMessageBox.warning(self, "No WAV files", "Drop at least one .wav file.")
            return

        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "Please wait", "A conversion is already running.")
            return

        self.progress.setRange(0, 0)
        self.progress.show()
        output_text = f" to {self.output_dir}" if self.output_dir else " in the WAV files folder"
        self.status.setText(f"Converting {len(wav_files)} file(s){output_text}...")

        self.worker = ConversionWorker(wav_files, ignored, self.output_dir)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.start()

    def on_conversion_finished(self, level: str, message: str) -> None:
        self.progress.hide()
        self.progress.setRange(0, 1)
        self.progress.setValue(0)
        self.status.setText("Done." if level != "error" else "Done with errors.")

        if level == "error":
            QMessageBox.critical(self, APP_NAME, message)
        else:
            QMessageBox.information(self, APP_NAME, message)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor, QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
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

MODERN_DARK_STYLE = """
QMainWindow {
    background: #070b14;
}
QWidget#appShell {
    background: #070b14;
    color: #f8fafc;
    font-family: "Inter", "SF Pro Display", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}
QFrame#heroCard {
    background: #0f172a;
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 32px;
}
QLabel#eyebrow {
    color: #38bdf8;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.8px;
    text-transform: uppercase;
}
QLabel#title {
    color: #f8fafc;
    font-size: 34px;
    font-weight: 850;
    letter-spacing: -0.8px;
}
QLabel#subtitle {
    color: #94a3b8;
    font-size: 15px;
    line-height: 1.45;
}
QFrame#outputCard {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 18px;
}
QLabel#outputLabel {
    color: #cbd5e1;
    font-size: 13px;
    font-weight: 600;
}
QFrame#dropCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #111827, stop:1 #0b1220);
    border: 1px dashed rgba(56, 189, 248, 0.72);
    border-radius: 28px;
}
QFrame#dropCard[dragging="true"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #082f49, stop:1 #0f172a);
    border: 2px solid #38bdf8;
}
QLabel#dropIcon {
    color: #7dd3fc;
    font-size: 42px;
    font-weight: 700;
}
QLabel#dropLabel {
    color: #f8fafc;
    font-size: 22px;
    font-weight: 800;
}
QLabel#dropHint {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 500;
}
QLabel#status {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 600;
    padding-left: 12px;
}
QPushButton {
    border: 0;
    border-radius: 14px;
    padding: 12px 18px;
    font-size: 13px;
    font-weight: 800;
}
QPushButton#primaryButton {
    color: #04111f;
    background: #38bdf8;
}
QPushButton#primaryButton:hover {
    background: #7dd3fc;
}
QPushButton#primaryButton:pressed {
    background: #0ea5e9;
}
QPushButton#secondaryButton {
    color: #e2e8f0;
    background: rgba(30, 41, 59, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.20);
}
QPushButton#secondaryButton:hover {
    background: rgba(51, 65, 85, 0.98);
    border: 1px solid rgba(125, 211, 252, 0.42);
}
QProgressBar {
    background: rgba(30, 41, 59, 0.9);
    border: 0;
    border-radius: 6px;
    height: 8px;
}
QProgressBar::chunk {
    background: #38bdf8;
    border-radius: 6px;
}
""".strip()


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
        self.setObjectName("dropCard")
        self.setMinimumHeight(210)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)
        layout.setContentsMargins(28, 28, 28, 28)

        icon = QLabel("WAV")
        icon.setAlignment(Qt.AlignCenter)
        icon.setObjectName("dropIcon")
        layout.addWidget(icon)

        label = QLabel("Drop WAV files here")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("dropLabel")
        layout.addWidget(label)

        hint = QLabel("Batch convert to high-quality MP3 in seconds")
        hint.setAlignment(Qt.AlignCenter)
        hint.setObjectName("dropHint")
        layout.addWidget(hint)

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
        self.resize(760, 560)
        self.setMinimumSize(660, 500)

        central = QWidget()
        central.setObjectName("appShell")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(18)

        hero = QFrame()
        hero.setObjectName("heroCard")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(28, 26, 28, 24)
        hero_layout.setSpacing(10)
        layout.addWidget(hero)

        eyebrow = QLabel("AUDIO CONVERTER")
        eyebrow.setObjectName("eyebrow")
        eyebrow.setAlignment(Qt.AlignCenter)
        hero_layout.addWidget(eyebrow)

        title = QLabel(APP_NAME)
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        hero_layout.addWidget(title)

        subtitle = QLabel("Drop WAV files, choose where the MP3s go, and convert them with a clean native desktop app.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        hero_layout.addWidget(subtitle)

        output_card = QFrame()
        output_card.setObjectName("outputCard")
        output_row = QHBoxLayout(output_card)
        output_row.setContentsMargins(14, 12, 14, 12)
        output_row.setSpacing(12)
        layout.addWidget(output_card)

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
        bottom.setSpacing(14)
        bottom.setContentsMargins(0, 8, 0, 0)
        layout.addLayout(bottom)

        choose_button = QPushButton("Choose WAV files")
        choose_button.clicked.connect(self.choose_files)
        choose_button.setObjectName("primaryButton")
        bottom.addWidget(choose_button)

        self.status = QLabel("Ready.")
        self.status.setObjectName("status")
        bottom.addWidget(self.status, stretch=1)

        self.setStyleSheet(MODERN_DARK_STYLE)
        self._add_shadow(hero, blur=38, offset_y=18, alpha=90)
        self._add_shadow(self.drop_zone, blur=28, offset_y=14, alpha=64)

    def _add_shadow(self, widget: QWidget, blur: int, offset_y: int, alpha: int) -> None:
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, offset_y)
        shadow.setColor(QColor(0, 0, 0, alpha))
        shadow.setEnabled(True)
        widget.setGraphicsEffect(shadow)

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

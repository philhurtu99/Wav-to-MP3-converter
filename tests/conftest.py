import sys

import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture
def qapp():
    app = QApplication.instance() or QApplication(sys.argv)
    yield app

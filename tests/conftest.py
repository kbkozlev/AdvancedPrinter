import io

import pytest


class Terminal(io.StringIO):
    def isatty(self):
        return True


@pytest.fixture(autouse=True)
def clean_color_environment(monkeypatch):
    for key in ("NO_COLOR", "TERM", "COLORTERM", "WT_SESSION", "ANSICON"):
        monkeypatch.delenv(key, raising=False)


@pytest.fixture
def terminal(monkeypatch):
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setenv("WT_SESSION", "test")
    return Terminal()

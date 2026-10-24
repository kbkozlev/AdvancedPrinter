import io
import sys
from types import SimpleNamespace

import pytest

import advancedprinter.terminal as terminal_module
from advancedprinter import Printer, strip_ansi
from advancedprinter.terminal import _windows_vt, capabilities


@pytest.mark.parametrize(
    "term,colorterm,expected",
    [
        ("xterm", "", "standard"),
        ("xterm-256color", "", "256"),
        ("xterm", "truecolor", "truecolor"),
        ("xterm", "24bit", "truecolor"),
    ],
)
def test_automatic_depth(terminal, monkeypatch, term, colorterm, expected):
    monkeypatch.setenv("TERM", term)
    monkeypatch.setenv("COLORTERM", colorterm)
    assert capabilities(terminal, "auto", "auto") == (True, True, expected)


def test_stream_without_isatty():
    assert capabilities(object(), "auto", "auto")[:2] == (False, False)


def test_broken_isatty():
    class Broken:
        def isatty(self):
            raise OSError("closed")

    assert capabilities(Broken(), "auto", "auto")[:2] == (False, False)


@pytest.mark.parametrize("supported", [False, True])
def test_windows_console_detection(terminal, monkeypatch, supported):
    monkeypatch.delenv("WT_SESSION", raising=False)
    monkeypatch.setattr(terminal_module, "os", SimpleNamespace(name="nt", environ={}))
    monkeypatch.setattr(terminal_module, "_windows_vt", lambda stream: supported)
    assert capabilities(terminal, "auto", "standard")[:2] == (supported, supported)


def test_windows_vt_enables_processing_without_losing_flags(monkeypatch):
    called = []
    mode = SimpleNamespace(value=3)
    kernel = SimpleNamespace(
        GetConsoleMode=lambda handle, pointer: 1,
        SetConsoleMode=lambda handle, value: called.append((handle, value)) or 1,
    )
    monkeypatch.setitem(sys.modules, "msvcrt", SimpleNamespace(get_osfhandle=lambda fd: 123))
    monkeypatch.setitem(
        sys.modules,
        "ctypes",
        SimpleNamespace(
            c_ulong=lambda: mode,
            c_void_p=lambda value: value,
            byref=lambda value: value,
            windll=SimpleNamespace(kernel32=kernel),
        ),
    )
    stream = SimpleNamespace(fileno=lambda: 1)
    assert _windows_vt(stream)
    assert called == [(123, 7)]


def test_windows_vt_failure_is_plain(monkeypatch):
    monkeypatch.setitem(sys.modules, "msvcrt", SimpleNamespace())
    assert not _windows_vt(io.StringIO())


def test_ascii_border_fallback_and_no_color(monkeypatch):
    class ASCIIStream(io.StringIO):
        @property
        def encoding(self):
            return "ascii"

        def isatty(self):
            return True

    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setenv("WT_SESSION", "test")
    output = ASCIIStream()
    Printer(file=output).frame("hello", border="double", c="red", s="b")
    assert strip_ansi(output.getvalue()).startswith("+")
    assert "\x1b[31m" not in output.getvalue()


def test_per_call_policy_and_depth_override():
    output = io.StringIO()
    Printer(file=output).print("x", c="#ff0000", color_mode="always", color_system="256")
    assert "\x1b[38;5;9m" in output.getvalue()

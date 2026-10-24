"""Destination-aware colour policy and ANSI helpers."""

from __future__ import annotations

import os
import re
from typing import TextIO

from .styles import validate_policy

# CSI, OSC (including hyperlinks), and simple two-byte escape sequences.
ANSI_RE = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07\x1b]*(?:\x07|\x1b\\)|[@-_])")
SGR_RE = re.compile(r"\x1b\[([0-9;]*)m")


def strip_ansi(text: str) -> str:
    """Remove terminal escape sequences, leaving the printable text."""
    return ANSI_RE.sub("", text)


def _windows_vt(stream: TextIO) -> bool:
    """Enable native VT processing on Windows console streams when possible."""
    try:
        import ctypes
        import msvcrt

        handle = msvcrt.get_osfhandle(stream.fileno())  # type: ignore[attr-defined]
        mode = ctypes.c_ulong()
        kernel = ctypes.windll.kernel32  # type: ignore[attr-defined]
        handle_pointer = ctypes.c_void_p(handle)
        return bool(
            kernel.GetConsoleMode(handle_pointer, ctypes.byref(mode))
            and kernel.SetConsoleMode(handle_pointer, mode.value | 4)
        )
    except (ImportError, AttributeError, OSError, ValueError):
        return False


def capabilities(stream: TextIO, mode: str, system: str) -> tuple[bool, bool, str]:
    """Return (styling enabled, colours enabled, resolved colour depth)."""
    validate_policy(mode, system)
    if mode == "never":
        return False, False, "standard"
    if mode == "always":
        return True, True, "truecolor" if system == "auto" else system
    try:
        tty = stream.isatty()
    except (AttributeError, OSError, ValueError):
        tty = False
    enabled = bool(tty) and os.environ.get("TERM") != "dumb"
    if enabled and os.name == "nt":
        enabled = bool(
            os.environ.get("WT_SESSION") or os.environ.get("ANSICON") or _windows_vt(stream)
        )
    colors = enabled and not bool(os.environ.get("NO_COLOR"))
    if system == "auto":
        if os.environ.get("COLORTERM", "").lower() in ("truecolor", "24bit"):
            system = "truecolor"
        elif "256color" in os.environ.get("TERM", ""):
            system = "256"
        else:
            system = "standard"
    return enabled, colors, system


def strip_colors(text: str) -> str:
    """Remove SGR colours but retain attributes such as bold (NO_COLOR)."""

    def replace(match: re.Match[str]) -> str:
        parameters = (match[1] or "0").split(";")
        kept: list[str] = []
        i = 0
        while i < len(parameters):
            number = int(parameters[i] or "0")
            if number in (38, 48, 58) and i + 1 < len(parameters):
                i += 5 if parameters[i + 1] == "2" else 3
                continue
            if not (30 <= number <= 49 or 90 <= number <= 107 or number == 59):
                kept.append(parameters[i])
            i += 1
        return "\x1b[" + ";".join(kept) + "m" if kept else ""

    return SGR_RE.sub(replace, text)

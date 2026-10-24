"""An adapter for Python logging; records are never modified."""

from __future__ import annotations

import copy
import logging
import sys
from typing import TextIO

from .render import _render
from .styles import validate_policy
from .terminal import capabilities


class ColorFormatter(logging.Formatter):
    """Colour a formatted log record for an explicitly associated stream.

    Set stream= to the same stream as the logging.StreamHandler. Use an ordinary
    logging.Formatter on file handlers; each handler keeps its own formatting.
    """

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        *,
        stream: TextIO | None = None,
        color_mode: str = "auto",
        color_system: str = "auto",
    ) -> None:
        super().__init__(fmt, datefmt)
        validate_policy(color_mode, color_system)
        self.stream = stream
        self.color_mode = color_mode
        self.color_system = color_system

    def format(self, record: logging.LogRecord) -> str:
        text = super().format(copy.copy(record))
        enabled, colors, system = capabilities(
            self.stream if self.stream is not None else sys.stderr,
            self.color_mode,
            self.color_system,
        )
        if record.levelno >= logging.ERROR:
            color, style = "red", "bold"
        elif record.levelno >= logging.WARNING:
            color, style = "yellow", None
        elif record.levelno >= logging.INFO:
            color, style = "cyan1", None
        else:
            color, style = "gray", None
        return _render(text, c=color, s=style, enabled=enabled, colors=colors, system=system)

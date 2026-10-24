"""Stream-aware printing and independently configurable printer instances."""

from __future__ import annotations

import builtins
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TextIO, cast

from .render import _join, _render, format_frame, format_text
from .styles import BACKGROUNDS, FOREGROUNDS, STYLES, Color, Style, alias, validate_policy
from .terminal import capabilities, strip_ansi, strip_colors


@dataclass(frozen=True)
class MessageStyle:
    """Theme entry for a semantic message; the prefix remains in plain output."""

    color: Color = None
    style: Style = None
    prefix: str = ""


DEFAULT_THEME: Mapping[str, MessageStyle] = {
    "success": MessageStyle("green2", prefix="[SUCCESS]"),
    "warning": MessageStyle("yellow", prefix="[WARNING]"),
    "error": MessageStyle("red", "bold", "[ERROR]"),
    "info": MessageStyle("cyan1", prefix="[INFO]"),
}


class Printer:
    """A printer with per-instance policy, streams, and semantic message theme.

    file=None resolves sys.stdout at call time; error_file=None resolves
    sys.stderr for error(). Explicit per-call file= always takes precedence.
    """

    def __init__(
        self,
        *,
        color_mode: str = "auto",
        color_system: str = "auto",
        file: TextIO | None = None,
        error_file: TextIO | None = None,
        theme: Mapping[str, MessageStyle] | None = None,
    ) -> None:
        validate_policy(color_mode, color_system)
        self.color_mode = color_mode
        self.color_system = color_system
        self.file = file
        self.error_file = error_file
        self.theme = dict(DEFAULT_THEME)
        if theme:
            if set(theme) - set(DEFAULT_THEME):
                raise ValueError("Theme keys must be success, warning, error, or info")
            if not all(isinstance(entry, MessageStyle) for entry in theme.values()):
                raise TypeError("Theme values must be MessageStyle instances")
            self.theme.update(theme)

    def _stream(self, file: TextIO | None = None) -> TextIO:
        return file if file is not None else self.file if self.file is not None else sys.stdout

    def print(
        self,
        *values: object,
        c: Color = None,
        b: Color = None,
        s: Style = None,
        color: Color = None,
        background: Color = None,
        style: Style = None,
        sep: str | None = " ",
        end: str | None = "\n",
        file: TextIO | None = None,
        flush: bool = False,
        color_mode: str | None = None,
        color_system: str | None = None,
    ) -> None:
        """Print with built-in sep/end/file/flush semantics and optional styling."""
        stream = self._stream(file)
        enabled, colors, system = capabilities(
            stream,
            self.color_mode if color_mode is None else color_mode,
            self.color_system if color_system is None else color_system,
        )
        c = cast(Color, alias(c, color, "c", "color"))
        b = cast(Color, alias(b, background, "b", "background"))
        s = cast(Style, alias(s, style, "s", "style"))
        text = _render(
            _join(values, sep), c=c, b=b, s=s, enabled=enabled, colors=colors, system=system
        )
        if isinstance(end, str):
            end = strip_ansi(end) if not enabled else strip_colors(end) if not colors else end
        builtins.print(text, end=end, file=stream, flush=flush)

    # Pure operations intentionally retain their explicit/default ANSI policy.
    format_text = staticmethod(format_text)
    line = staticmethod(format_text)
    format_frame = staticmethod(format_frame)

    def frame(
        self,
        text: object,
        f_s: str | None = None,
        f_c: Color = None,
        f_b: Color = None,
        c: Color = None,
        b: Color = None,
        s: Style = None,
        *,
        border: str | None = None,
        border_color: Color = None,
        border_background: Color = None,
        color: Color = None,
        background: Color = None,
        style: Style = None,
        title: str = "",
        padding: int = 1,
        width: int | None = None,
        max_width: int | None = None,
        wrap: bool = True,
        align: str = "left",
        dedent: bool = False,
        ascii: bool = False,
        file: TextIO | None = None,
        end: str | None = "\n",
        flush: bool = False,
        color_mode: str | None = None,
        color_system: str | None = None,
    ) -> None:
        """Print format_frame() output, applying this destination's colour policy."""
        stream = self._stream(file)
        enabled, colors, system = capabilities(
            stream,
            self.color_mode if color_mode is None else color_mode,
            self.color_system if color_system is None else color_system,
        )

        def render(use_ascii: bool) -> str:
            result = format_frame(
                text,
                f_s,
                f_c,
                f_b,
                c,
                b,
                s,
                border=border,
                border_color=border_color,
                border_background=border_background,
                color=color,
                background=background,
                style=style,
                title=title,
                padding=padding,
                width=width,
                max_width=max_width,
                wrap=wrap,
                align=align,
                dedent=dedent,
                ascii=use_ascii,
                color_mode="always" if enabled else "never",
                color_system=system,
            )
            return strip_colors(result) if not colors and enabled else result

        rendered = render(ascii)
        # Use ASCII borders automatically if the destination cannot encode them.
        encoding = getattr(stream, "encoding", None)
        if encoding:
            try:
                rendered.encode(encoding)
            except (UnicodeEncodeError, LookupError):
                rendered = render(True)
        if isinstance(end, str):
            end = strip_ansi(end) if not enabled else strip_colors(end) if not colors else end
        builtins.print(rendered, file=stream, end=end, flush=flush)

    def input(
        self,
        prompt: object = "",
        /,
        *,
        c: Color = None,
        b: Color = None,
        s: Style = None,
        color: Color = None,
        background: Color = None,
        style: Style = None,
    ) -> str:
        """Read input after writing an unmodified, optionally styled prompt."""
        self.print(
            prompt,
            c=c,
            b=b,
            s=s,
            color=color,
            background=background,
            style=style,
            end="",
            flush=True,
        )
        return builtins.input()

    def _message(
        self,
        kind: str,
        values: tuple[object, ...],
        *,
        file: TextIO | None = None,
        sep: str | None = " ",
        end: str | None = "\n",
        flush: bool = False,
    ) -> None:
        entry = self.theme[kind]
        text = _join(values, sep)
        if entry.prefix:
            text = entry.prefix + (" " + text if text else "")
        if kind == "error" and file is None:
            file = self.error_file if self.error_file is not None else sys.stderr
        self.print(text, color=entry.color, style=entry.style, file=file, end=end, flush=flush)

    def success(
        self,
        *values: object,
        file: TextIO | None = None,
        sep: str | None = " ",
        end: str | None = "\n",
        flush: bool = False,
    ) -> None:
        self._message("success", values, file=file, sep=sep, end=end, flush=flush)

    def warning(
        self,
        *values: object,
        file: TextIO | None = None,
        sep: str | None = " ",
        end: str | None = "\n",
        flush: bool = False,
    ) -> None:
        self._message("warning", values, file=file, sep=sep, end=end, flush=flush)

    def error(
        self,
        *values: object,
        file: TextIO | None = None,
        sep: str | None = " ",
        end: str | None = "\n",
        flush: bool = False,
    ) -> None:
        self._message("error", values, file=file, sep=sep, end=end, flush=flush)

    def info(
        self,
        *values: object,
        file: TextIO | None = None,
        sep: str | None = " ",
        end: str | None = "\n",
        flush: bool = False,
    ) -> None:
        self._message("info", values, file=file, sep=sep, end=end, flush=flush)

    def help(self, *, file: TextIO | None = None) -> None:
        """Show the palette and style names using the destination colour policy."""
        self.print("Text Colors:", file=file)
        for name in FOREGROUNDS:
            self.print("- " + name, c=name, file=file)
        self.print("\nBackground Colors:", file=file)
        for name in BACKGROUNDS:
            self.print("- " + name, b=name, file=file)
        self.print("\nAvailable styles:", file=file)
        for name in STYLES:
            self.print("- " + name, s=name, file=file)

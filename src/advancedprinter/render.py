"""Pure rendering functions: no output streams or global configuration."""

from __future__ import annotations

import re
import textwrap
from typing import cast

from wcwidth import iter_graphemes, wcswidth
from wcwidth import wrap as cell_wrap

from .styles import RESET, Color, Style, alias, color_code, style_code, validate_policy
from .terminal import SGR_RE, strip_ansi, strip_colors


def visible_width(text: str) -> int:
    """Measure printable terminal cells, ignoring ANSI; reject control characters."""
    measured = wcswidth(strip_ansi(text))
    if measured < 0:
        raise ValueError("Frame content contains a non-printable control character")
    return measured


def _restore(text: str, foreground: str, background: str, styles: str) -> str:
    prefix = background + styles + foreground
    resets = {22: "\x1b[1m", 23: "\x1b[3m", 24: "\x1b[4m", 27: "\x1b[7m", 29: "\x1b[9m"}

    def restore(found: re.Match[str]) -> str:
        parameters = (found[1] or "0").split(";")
        output = ""
        i = 0
        while i < len(parameters):
            number = int(parameters[i] or "0")
            if number in (38, 48, 58) and i + 1 < len(parameters):
                size = 5 if parameters[i + 1] == "2" else 3
                output += "\x1b[" + ";".join(parameters[i : i + size]) + "m"
                i += size
                continue
            code = f"\x1b[{number}m"
            if number == 0:
                code += prefix
            elif number == 39:
                code += foreground
            elif number == 49:
                code += background
            elif number in resets and resets[number] in styles:
                code += resets[number]
            output += code
            i += 1
        return output

    return SGR_RE.sub(restore, text)


def _render(
    text: str,
    *,
    c: Color = None,
    b: Color = None,
    s: Style = None,
    enabled: bool = True,
    colors: bool = True,
    system: str = "truecolor",
) -> str:
    fg = color_code(c, system=system)
    bg = color_code(b, background=True, system=system)
    styles = style_code(s)
    if not enabled:
        return strip_ansi(text)
    if not colors:
        fg = bg = ""
        text = strip_colors(text)
    prefix = bg + styles + fg
    if not prefix:
        return text
    # Restore the enclosing style after an embedded line()/format_text() reset.
    return prefix + _restore(text, fg, bg, styles) + RESET


def _join(values: tuple[object, ...], sep: str | None) -> str:
    if sep is None:
        sep = " "
    if not isinstance(sep, str):
        raise TypeError(f"sep must be None or a string, not {type(sep).__name__}")
    return sep.join(str(value) for value in values)


def format_text(
    *values: object,
    c: Color = None,
    b: Color = None,
    s: Style = None,
    color: Color = None,
    background: Color = None,
    style: Style = None,
    sep: str | None = " ",
    end: str = "",
    color_mode: str = "always",
    color_system: str = "truecolor",
) -> str:
    """Return styled text. Pure formatting defaults to explicit ANSI output.

    Use color_mode='never' for a plain string. Destination-aware policy belongs
    to Printer.print(), which can inspect the stream it actually writes to.
    """
    validate_policy(color_mode, color_system)
    if color_mode == "auto" or color_system == "auto":
        raise ValueError(
            "Pure formatting needs an explicit colour policy/depth; use Printer for auto"
        )
    if not isinstance(end, str):
        raise TypeError("end must be a string")
    c = cast(Color, alias(c, color, "c", "color"))
    b = cast(Color, alias(b, background, "b", "background"))
    s = cast(Style, alias(s, style, "s", "style"))
    return _render(
        _join(values, sep), c=c, b=b, s=s, enabled=color_mode != "never", system=color_system
    ) + (strip_ansi(end) if color_mode == "never" else end)


BORDERS = {
    "basic": ("-", "|", "++++"),
    "basic2": ("=", "#", "===="),
    "single": ("─", "│", "┌┐└┘"),
    "double": ("═", "║", "╔╗╚╝"),
    "rounded": ("─", "│", "╭╮╰╯"),
}


def format_frame(
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
    color_mode: str = "always",
    color_system: str = "truecolor",
) -> str:
    """Return a frame; width/max_width include borders and horizontal padding.

    Whitespace is preserved. Widths are terminal cells, not Python string length.
    Content too wide to fit with wrap=False raises ValueError.
    """
    validate_policy(color_mode, color_system)
    if color_mode == "auto" or color_system == "auto":
        raise ValueError("Pure formatting needs explicit colour policy/depth")
    border = cast(str | None, alias(f_s, border, "f_s", "border"))
    if border is None:
        border = "basic"
    c = cast(Color, alias(c, color, "c", "color"))
    b = cast(Color, alias(b, background, "b", "background"))
    s = cast(Style, alias(s, style, "s", "style"))
    f_c = cast(Color, alias(f_c, border_color, "f_c", "border_color"))
    f_b = cast(Color, alias(f_b, border_background, "f_b", "border_background"))
    if border not in BORDERS:
        raise ValueError(f"Unknown border {border!r}; choose from {', '.join(BORDERS)}")
    if type(padding) is not int or padding < 0:
        raise ValueError("padding must be a non-negative integer")
    if align not in ("left", "center", "right"):
        raise ValueError("align must be 'left', 'center', or 'right'")
    if not isinstance(title, str) or "\n" in title or "\r" in title:
        raise ValueError("title must be a single-line string")
    for value in (width, max_width):
        if value is not None and (type(value) is not int or value < 2 + 2 * padding + 1):
            raise ValueError("Frame width must leave at least one cell for content")
    if width is not None and max_width is not None and width > max_width:
        raise ValueError("width cannot exceed max_width")
    raw = str(text).replace("\r\n", "\n").expandtabs(4)
    if dedent:
        raw = textwrap.dedent(raw)
    lines = raw.split("\n")
    content_width = max(1, *(visible_width(line) for line in lines))
    title_width = visible_width(title) + 2 if title else 0
    natural_width = max(content_width + 2 * padding, title_width) + 2
    total = width if width is not None else min(natural_width, max_width or natural_width)
    available = total - 2 - 2 * padding
    if title_width > total - 2:
        raise ValueError("title is too wide for the frame")
    rendered_lines: list[str] = []
    for line in lines:
        if visible_width(line) > available:
            if not wrap:
                raise ValueError("Content exceeds frame width; enable wrap or increase width")
            if any(wcswidth(cluster) > available for cluster in iter_graphemes(strip_ansi(line))):
                raise ValueError("A character is wider than the available frame content width")
            rendered_lines.extend(
                cell_wrap(
                    line,
                    width=available,
                    drop_whitespace=False,
                    replace_whitespace=False,
                    break_on_hyphens=False,
                )
            )
        else:
            rendered_lines.append(line)
    horizontal, vertical, corners = BORDERS["basic" if ascii else border]
    frame_fg = c if f_c is None else f_c
    frame_bg = b if f_b is None else f_b
    enabled = color_mode != "never"

    def edge(value: str) -> str:
        return _render(value, c=frame_fg, b=frame_bg, enabled=enabled, system=color_system)

    top_fill = (" " + title + " ") if title else ""
    top = edge(corners[0] + top_fill + horizontal * (total - 2 - title_width) + corners[1])
    output = [top]
    for line in rendered_lines:
        remaining = available - visible_width(line)
        left = remaining if align == "right" else remaining // 2 if align == "center" else 0
        padded = " " * left + line + " " * (remaining - left)
        body = _render(padded, c=c, b=b, s=s, enabled=enabled, system=color_system)
        output.append(edge(vertical + " " * padding) + body + edge(" " * padding + vertical))
    output.append(edge(corners[2] + horizontal * (total - 2) + corners[3]))
    return "\n".join(output)

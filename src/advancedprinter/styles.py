"""Validated style and colour specifications, with legacy palette names."""

from __future__ import annotations

import re
from typing import Literal, TypeAlias

from ._codes import Codes

Color: TypeAlias = str | int | tuple[int, int, int] | None
Style: TypeAlias = str | tuple[str, ...] | list[str] | None
ColorMode: TypeAlias = Literal["auto", "always", "never"]
ColorSystem: TypeAlias = Literal["auto", "standard", "256", "truecolor"]

RESET = "\x1b[0m"
# Keep separate registries: a style name cannot accidentally be used as a colour.
_NAMES = (
    "black white red red1 red2 green green1 green2 green3 yellow yellow1 yellow2 "
    "olive blue blue1 blue2 blue3 magenta magenta1 pink purple cyan cyan1 cyan2 orange gray gray1"
).split()
_BG_NAMES = (
    "black white gray gray1 red red1 green green1 yellow olive blue blue1 magenta pink "
    "cyan cyan1 orange orange1 brown"
).split()
FOREGROUNDS: dict[str, str] = {name: getattr(Codes, name.upper()) for name in _NAMES}
BACKGROUNDS: dict[str, str] = {name: getattr(Codes, "BG_" + name.upper()) for name in _BG_NAMES}
STYLES = {"bold": 1, "italic": 3, "underline": 4, "inverted": 7, "strike-through": 9}
_ALIASES = {
    "b": "bold",
    "it": "italic",
    "u": "underline",
    "inv": "inverted",
    "str": "strike-through",
    "strikethrough": "strike-through",
    "strike": "strike-through",
}
# xterm's conventional ANSI palette; actual terminal themes can differ.
_PALETTE = (
    (0, 0, 0),
    (128, 0, 0),
    (0, 128, 0),
    (128, 128, 0),
    (0, 0, 128),
    (128, 0, 128),
    (0, 128, 128),
    (192, 192, 192),
    (128, 128, 128),
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
)


def alias(short: object, long: object, short_name: str, long_name: str) -> object:
    """Reject conflicting spellings rather than silently choosing one."""
    if short is not None and long is not None and short != long:
        raise TypeError(f"Use either {short_name}= or {long_name}=, not conflicting values")
    return long if long is not None else short


def validate_policy(mode: str, system: str) -> None:
    if mode not in ("auto", "always", "never"):
        raise ValueError("color_mode must be 'auto', 'always', or 'never'")
    if system not in ("auto", "standard", "256", "truecolor"):
        raise ValueError("color_system must be 'auto', 'standard', '256', or 'truecolor'")


def _index_rgb(index: int) -> tuple[int, int, int]:
    if index < 16:
        return _PALETTE[index]
    if index >= 232:
        n = 8 + (index - 232) * 10
        return n, n, n
    index -= 16
    levels = (0, 95, 135, 175, 215, 255)
    return levels[index // 36], levels[(index // 6) % 6], levels[index % 6]


def _nearest(rgb: tuple[int, int, int], limit: int) -> int:
    return min(
        range(limit),
        key=lambda i: sum((a - b) ** 2 for a, b in zip(rgb, _index_rgb(i), strict=True)),
    )


def color_code(value: Color, *, background: bool = False, system: str = "truecolor") -> str:
    """Accept palette names, #RRGGBB, RGB tuples, or xterm indexes 0..255."""
    if value is None:
        return ""
    prefix = 48 if background else 38
    registry = BACKGROUNDS if background else FOREGROUNDS
    if isinstance(value, str):
        key = value.lower()
        if key == "default":
            return "\x1b[49m" if background else "\x1b[39m"
        if key in registry:
            code = registry[key]
            parameters = [int(p) for p in code[2:-1].split(";")]
            if len(parameters) == 1:
                return code
            value = tuple(parameters[2:]) if parameters[1] == 2 else parameters[2]  # type: ignore[assignment]
        elif re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            value = tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))  # type: ignore[assignment]
        else:
            raise ValueError(
                f"Unknown {'background' if background else 'foreground'} colour {value!r}"
            )
    if isinstance(value, bool):
        raise ValueError("Colour indexes must be integers from 0 to 255, not booleans")
    if isinstance(value, int):
        if not 0 <= value <= 255:
            raise ValueError("Colour index must be between 0 and 255")
        if system != "standard":
            return f"\x1b[{prefix};5;{value}m"
        rgb = _index_rgb(value)
    elif (
        isinstance(value, tuple)
        and len(value) == 3
        and all(type(channel) is int and 0 <= channel <= 255 for channel in value)
    ):
        rgb = value
        if system == "truecolor":
            return f"\x1b[{prefix};2;{rgb[0]};{rgb[1]};{rgb[2]}m"
        if system == "256":
            return f"\x1b[{prefix};5;{_nearest(rgb, 256)}m"
    else:
        raise ValueError("Colour must be a name, #RRGGBB, RGB tuple, or index 0..255")
    index = _nearest(rgb, 16)
    base = 40 if background else 30
    return f"\x1b[{base + index if index < 8 else base + 60 + index - 8}m"


def style_code(value: Style) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        # Preserve the hyphenated full name while supporting legacy 'b-it-u'.
        tokens = value.lower().replace("strike-through", "strikethrough").replace(",", " ").split()
        tokens = [part for token in tokens for part in token.split("-")]
    elif isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
        tokens = [item.lower() for item in value]
    else:
        raise TypeError("style must be a string or sequence of style names")
    codes: list[int] = []
    for token in tokens:
        name = _ALIASES.get(token, token)
        if name not in STYLES:
            raise ValueError(f"Unknown style {token!r}; choose from {', '.join(STYLES)}")
        if STYLES[name] not in codes:
            codes.append(STYLES[name])
    return "".join(f"\x1b[{code}m" for code in codes)

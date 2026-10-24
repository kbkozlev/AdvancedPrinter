"""Render the visual examples' actual ANSI output into documentation PNGs.

Install the optional dependencies with: python -m pip install '.[screenshots]'
Run: python scripts/render_examples.py

This is an offline terminal rendering, not an operating-system window capture.
pyte interprets the real ANSI stream; Pillow draws the resulting terminal cells.
The default font is DejaVu Sans Mono (as packaged on Debian/Ubuntu). Pass
--font-dir to use another directory containing the same four font filenames.
"""

from __future__ import annotations

import argparse
import math
import os
import subprocess
import sys
from pathlib import Path

import pyte
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = {
    "colours": ("colours-and-styles.png", "Colours and styles"),
    "inline": ("inline-and-nested-styles.png", "Inline and nested styles"),
    "frames": ("frames-and-wrapping.png", "Frames and wrapping"),
    "messages": ("messages-and-logging.png", "Messages, themes and logging"),
    "output-policy": ("terminal-and-log-file.png", "Terminal output and log files"),
}
BACKGROUND = "#111927"
FOREGROUND = "#dde7f3"
PALETTE = {
    "black": "#111927",
    "red": "#ef6a72",
    "green": "#82c99b",
    "brown": "#e5c07b",
    "blue": "#6aa7f4",
    "magenta": "#bf90e7",
    "cyan": "#6fd1dd",
    "white": "#d5dce6",
    "brightblack": "#73839a",
    "brightred": "#ff8189",
    "brightgreen": "#8de4a3",
    "brightyellow": "#ffe08c",
    "brightbrown": "#ffe08c",
    "brightblue": "#93bbff",
    "brightmagenta": "#ddb2ff",
    "brightcyan": "#89e4f3",
    "brightwhite": "#ffffff",
}


def terminal_color(value: str, default: str) -> str:
    if value == "default":
        return default
    if value in PALETTE:
        return PALETTE[value]
    if len(value) == 6 and all(char in "0123456789abcdef" for char in value.lower()):
        return "#" + value
    raise ValueError(f"Unexpected terminal colour {value!r}")


def capture(section: str) -> str:
    environment = dict(os.environ)
    environment.pop("NO_COLOR", None)
    environment.update(
        TERM="xterm-256color",
        COLORTERM="truecolor",
        WT_SESSION="advancedprinter-documentation",
        PYTHONIOENCODING="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-u",
            str(ROOT / "examples" / "visual_examples.py"),
            section,
            "--color-mode",
            "always",
        ],
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout


def render(section: str, title: str, text: str, destination: Path, font_dir: Path) -> None:
    fonts = {
        (False, False): ImageFont.truetype(str(font_dir / "DejaVuSansMono.ttf"), 22),
        (True, False): ImageFont.truetype(str(font_dir / "DejaVuSansMono-Bold.ttf"), 22),
        (False, True): ImageFont.truetype(str(font_dir / "DejaVuSansMono-Oblique.ttf"), 22),
        (True, True): ImageFont.truetype(str(font_dir / "DejaVuSansMono-BoldOblique.ttf"), 22),
    }
    regular = fonts[False, False]
    small = ImageFont.truetype(str(font_dir / "DejaVuSansMono.ttf"), 14)
    screen = pyte.Screen(80, 100)
    stream = pyte.Stream(screen)
    stream.feed(text.replace("\r\n", "\n").replace("\n", "\r\n"))
    used_rows = (
        max(
            (
                row
                for row, cells in screen.buffer.items()
                if any(cell.data.strip() or cell.bg != "default" for cell in cells.values())
            ),
            default=0,
        )
        + 1
    )
    if screen.cursor.y >= 99:
        raise ValueError("Example exceeded the screenshot terminal height")
    cell_width, row_height = regular.getlength("M"), 27
    padding, header, command_area, footer = 28, 54, 58, 48
    width = math.ceil(80 * cell_width) + padding * 2
    height = header + command_area + used_rows * row_height + padding + footer
    image = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, header), fill="#1d293b")
    draw.text((padding, 18), "AdvancedPrinter 2.0  /  " + title, font=small, fill=FOREGROUND)
    command = f"$ python examples/visual_examples.py {section} --color-mode always"
    draw.text((padding, header + 16), command, font=small, fill="#91a2ba")
    top = header + command_area
    for row in range(used_rows):
        for column in range(80):
            cell = screen.buffer[row][column]
            if not cell.data:
                continue
            foreground = terminal_color(cell.fg, FOREGROUND)
            background = terminal_color(cell.bg, BACKGROUND)
            if cell.reverse:
                foreground, background = background, foreground
            x, y = padding + column * cell_width, top + row * row_height
            if background != BACKGROUND:
                draw.rectangle((x, y, x + cell_width, y + row_height), fill=background)
            draw.text(
                (x, y + 21),
                cell.data,
                font=fonts[cell.bold, cell.italics],
                fill=foreground,
                anchor="ls",
            )
            if cell.underscore:
                draw.line((x, y + 23, x + cell_width, y + 23), fill=foreground, width=1)
            if cell.strikethrough:
                draw.line((x, y + 13, x + cell_width, y + 13), fill=foreground, width=1)
    draw.text(
        (padding, height - 29),
        "Rendered from actual example output | dark terminal theme",
        font=small,
        fill="#73839a",
    )
    image.save(destination, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-dir", type=Path, default=Path("/usr/share/fonts/truetype/dejavu"))
    parser.add_argument("--output-dir", type=Path, default=ROOT / "docs" / "images")
    arguments = parser.parse_args()
    arguments.output_dir.mkdir(parents=True, exist_ok=True)
    for section, (filename, title) in SECTIONS.items():
        output = capture(section)
        destination = arguments.output_dir / filename
        render(section, title, output, destination, arguments.font_dir)
        print(f"{section}: {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

"""Run one visual example, or run the complete gallery.

    python examples/visual_examples.py colours
    python examples/visual_examples.py all --color-mode always

Each example uses the public AdvancedPrinter API. No network access or input
is needed. Terminal policy uses simulated in-memory streams for a repeatable
TTY-versus-file comparison; it does not modify the caller's environment.
"""

from __future__ import annotations

import argparse
import io
import logging
import sys
from collections.abc import Callable

from advancedprinter import ColorFormatter, MessageStyle, Printer, format_frame, line, strip_ansi


def heading(console: Printer, title: str) -> None:
    console.print(title, color="cyan1", style="bold")
    console.print()


def colours(console: Printer) -> None:
    heading(console, "COLOURS AND STYLES")
    console.print("Normal text: the familiar print() behaviour")
    console.print("Success in bold", color="green2", style="bold")
    console.print("Hex colour: #ffaf5f", color="#ffaf5f")
    console.print("RGB colour: (190, 150, 255)", color=(190, 150, 255))
    console.print("Palette index: 45", color=45)
    console.print()
    console.print("Bold + italic + underline", style="bold italic underline")
    console.print("Strike-through text", style="strike-through")
    console.print("Inverted text", style="inverted")
    console.print(" White text on a blue background ", color="white", background="blue")
    console.print()
    console.print("Bitwarden", "Citrix", "Rambox", sep=" | ")


def inline(console: Printer) -> None:
    heading(console, "INLINE COLOURS AND NESTED STYLES")
    console.print("Hello, " + line("Kaloian", color="cyan2", style="bold") + "!")
    console.print(
        line("3 updated", color="green2")
        + "  /  "
        + line("1 cached", color="yellow1")
        + "  /  "
        + line("0 failed", color="red1")
    )
    console.print()
    console.print("Before " + line("inside", color="cyan2") + " after", color="red1")
    console.print("The outer red resumes after the cyan word.", color="gray1")
    console.print()
    formatted = line("Ready for export", color="green2", style="bold")
    console.print("Formatted string: " + formatted)
    console.print("Plain string:     " + strip_ansi(formatted))


def frames(console: Printer) -> None:
    heading(console, "FRAMES: TITLES, ALIGNMENT AND WRAPPING")
    console.frame(
        "Bitwarden   up to date\nCitrix      updated\nRambox      updated",
        title="Repository sync",
        border="rounded",
        border_color="cyan2",
        color="white",
        width=46,
    )
    console.print()
    console.frame(
        "All systems ready",
        title="Status",
        border="double",
        border_color="green2",
        color="green2",
        style="bold",
        align="center",
        width=46,
    )
    console.print()
    console.frame(
        "A long message wraps automatically inside the chosen width.\n"
        "    Indentation is preserved.",
        title="Wrapped message",
        border="single",
        border_color="yellow1",
        width=46,
    )
    console.print()
    saved = format_frame("This frame is a string", border="basic", color_mode="never")
    console.print(saved)


def messages(console: Printer) -> None:
    heading(console, "STATUS MESSAGES, THEMES AND LOGGING")
    console.success("Repository updated")
    console.info("Downloaded", 3, "packages")
    console.warning("Using cached release information")
    # Explicit stream keeps this demonstration ordered even when captured.
    console.error("Example failure: connection timed out", file=console.file)
    console.print()
    custom = Printer(
        color_mode=console.color_mode,
        color_system=console.color_system,
        file=console.file,
        theme={"success": MessageStyle("cyan2", "bold", "DONE")},
    )
    custom.success("A custom prefix and colour")
    console.print()
    handler = logging.StreamHandler(console.file or sys.stdout)
    handler.setFormatter(
        ColorFormatter(
            "%(levelname)s: %(message)s",
            stream=handler.stream,
            color_mode=console.color_mode,
            color_system=console.color_system,
        )
    )
    logger = logging.getLogger("advancedprinter-visual-demo")
    previous_level, previous_propagation = logger.level, logger.propagate
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.addHandler(handler)
    try:
        logger.debug("Checking local metadata")
        logger.info("Repository scan complete")
        logger.warning("Retrying one download")
        logger.error("Example failure: download unavailable")
    finally:
        logger.removeHandler(handler)
        logger.setLevel(previous_level)
        logger.propagate = previous_propagation
        handler.close()


def output_policy(console: Printer) -> None:
    heading(console, "AUTO MODE: COLOUR IN THE TERMINAL, CLEAN LOG FILES")

    class TerminalBuffer(io.StringIO):
        def isatty(self) -> bool:
            return True

    # Feed the real public API two destinations. The first simulates a TTY;
    # the second behaves like an ordinary redirected file. For deterministic
    # screenshots, auto-mode terminal support is already established by the
    # screenshot runner's TERM/COLORTERM settings.
    terminal_output, file_output = TerminalBuffer(), io.StringIO()
    auto = Printer(color_mode="auto", color_system="truecolor")
    auto.print("Repository updated", color="green2", style="bold", file=terminal_output)
    auto.print("Repository updated", color="green2", style="bold", file=file_output)
    console.print("Terminal destination (isatty=True):", color="gray1")
    console.print(terminal_output.getvalue(), end="")
    console.print()
    console.print("File destination (isatty=False):", color="gray1")
    console.print(file_output.getvalue(), end="")
    console.print()
    console.print("File contents, shown with repr():", color="gray1")
    console.print(repr(file_output.getvalue()))
    console.print("No ANSI escape codes in the file.", color="cyan2")


SECTIONS: dict[str, Callable[[Printer], None]] = {
    "colours": colours,
    "inline": inline,
    "frames": frames,
    "messages": messages,
    "output-policy": output_policy,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("section", nargs="?", default="all", choices=["all", *SECTIONS])
    parser.add_argument("--color-mode", choices=["auto", "always", "never"], default="auto")
    args = parser.parse_args()
    console = Printer(color_mode=args.color_mode, color_system="truecolor", file=sys.stdout)
    selected = SECTIONS.values() if args.section == "all" else [SECTIONS[args.section]]
    for index, example in enumerate(selected):
        if index:
            console.print("\n")
        example(console)


if __name__ == "__main__":
    main()

"""Small terminal printing helpers with a backwards-compatible class facade."""

from importlib.metadata import version

from .logging import ColorFormatter
from .main import AdvancedPrinter
from .printer import MessageStyle, Printer
from .render import format_frame, format_text, visible_width
from .styles import Color, ColorMode, ColorSystem, Style
from .terminal import strip_ansi

__version__ = version("AdvancedPrinter")

print = AdvancedPrinter.print
input = AdvancedPrinter.input
line = AdvancedPrinter.line
frame = AdvancedPrinter.frame
help = AdvancedPrinter.help
success = AdvancedPrinter.success
warning = AdvancedPrinter.warning
error = AdvancedPrinter.error
info = AdvancedPrinter.info

__all__ = [
    "AdvancedPrinter",
    "Printer",
    "MessageStyle",
    "ColorFormatter",
    "Color",
    "Style",
    "ColorMode",
    "ColorSystem",
    "__version__",
    "print",
    "input",
    "line",
    "frame",
    "help",
    "success",
    "warning",
    "error",
    "info",
    "format_text",
    "format_frame",
    "strip_ansi",
    "visible_width",
]

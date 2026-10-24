"""Compatibility facade for the original class and its import path."""

from ._codes import Codes
from .printer import Printer

_default = Printer()


class AdvancedPrinter:
    """Legacy class-style API; use Printer for independent configuration."""

    C = Codes
    print = staticmethod(_default.print)
    line = staticmethod(_default.line)
    input = staticmethod(_default.input)
    frame = staticmethod(_default.frame)
    help = staticmethod(_default.help)
    format_text = staticmethod(_default.format_text)
    format_frame = staticmethod(_default.format_frame)
    success = staticmethod(_default.success)
    warning = staticmethod(_default.warning)
    error = staticmethod(_default.error)
    info = staticmethod(_default.info)

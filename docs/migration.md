# Migrating from AdvancedPrinter 1.x to 2.0

Version 2.0 keeps the package name, class import, direct function imports, short
style parameters, original palette constants, and four original border designs.
There are deliberate behaviour changes:

1. **Python 3.10 or later is required.** Version 1.2 remains available for older
   interpreters. `wcwidth>=0.9,<1` is the sole runtime dependency.
2. **Printing detects the destination.** Files, pipes, captured output, unsupported
   Windows consoles, and `TERM=dumb` receive plain output by default. Use
   `print(..., color_mode="always")` or `Printer(color_mode="always")` when you
   explicitly need ANSI output. Non-empty `NO_COLOR` suppresses default colours.
3. **Options are validated.** Misspelled colours, styles, or borders now raise
   descriptive errors. They no longer silently disappear or select a basic border.
   Correct the typo; `None` means no requested formatting.
4. **Prompts and frames preserve whitespace.** The old `strip()` behaviour removed
   indentation and trailing spaces. Use `dedent=True` on a frame if indentation
   in a triple-quoted source string is incidental. Prompts are used exactly.
5. **`input()` accepts zero or one prompt.** Extra prompt arguments raise
   `TypeError`; the old version ignored all but the first. Non-string prompts
   are stringified consistently with Python input conventions.
6. **Plain text has no gratuitous reset.** `line("hello")` now returns `"hello"`.
   Code comparing raw bytes should account for this correction.
7. **Pure formatting is explicit.** `line()` / `format_text()` and
   `format_frame()` return ANSI strings by default, including when accessed
   through a Printer instance. Use `color_mode="never"` for plain strings.
   `auto` is only valid for output operations that have a destination stream.

`sep` now works correctly, empty frames are supported, frame widths ignore ANSI
codes and use terminal cells, and nested styling restores its enclosing style.
These corrections can change exact captured output. Review snapshots if your
application depended on the old formatting bugs.

Old usage continues to work:

```python
from advancedprinter import AdvancedPrinter as ap

ap.print("Hello", c="green", s="b-it")
ap.frame("Hello", "double", "red", None, "white", "blue", "u")
```

For new code prefer readable parameters and independently configurable printers:

```python
from advancedprinter import Printer

console = Printer(color_mode="auto")
console.print("Hello", color="green", style="bold italic")
console.frame(
    "Hello",
    border="double",
    border_color="red",
    color="white",
    background="blue",
    style="underline",
)
```

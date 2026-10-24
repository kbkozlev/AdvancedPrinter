# AdvancedPrinter 2.0: a visual guide

The familiar coloured `print()` is still there. Version 2.0 makes it easier to
configure, adds useful output helpers, and improves how frames and inline styles
behave. This guide shows the changes through runnable examples.

These images are **rendered from the demo's actual ANSI output** with a terminal
emulator and a consistent dark theme. They are not AI-generated illustrations
or captures of a particular operating system. Your terminal palette and fonts
can look different. The screenshots force colour so the examples remain visible
when captured; normal applications should generally use the default `auto` mode.

From a checkout of the repository, run the whole demonstration:

```bash
python -m pip install -e .
python examples/visual_examples.py all
```

Or run one section: `colours`, `inline`, `frames`, `messages`, or `output-policy`.
The exact command appears at the top of each image. The snippets below highlight
the main calls; [visual_examples.py](../examples/visual_examples.py) contains the
complete runnable versions, including labels and additional combinations.

## 1. Readable styling and custom colours

Colours and styles existed in 1.x. The new parts are readable parameter names,
full style names, and custom colours. Existing `c`, `b`, and `s` arguments still
work. Choose named colours, a hex string, an RGB tuple, or a palette index.

```python
from advancedprinter import Printer

console = Printer()
console.print("Success in bold", color="green2", style="bold")
console.print("Hex colour: #ffaf5f", color="#ffaf5f")
console.print("RGB colour: (190, 150, 255)", color=(190, 150, 255))
console.print("Palette index: 45", color=45)
console.print("Bold + italic + underline", style="bold italic underline")
console.print("Strike-through text", style="strike-through")
console.print(" White text on a blue background ", color="white", background="blue")
```

![Colours, styles, and custom colours](https://raw.githubusercontent.com/kbkozlev/AdvancedPrinter/083938fb4d15bb18e821719db1a0dc4c675d3a82/docs/images/colours-and-styles.png)

`color="green2"` is a bright terminal-palette green. A hex/RGB value specifies a
target colour; automatic output can approximate it for a terminal with fewer
colours. Italics and strike-through still depend on terminal/font support.

## 2. Inline text and reliable nested formatting

`line()` already returned a coloured string for use inside a sentence. It is now
also named `format_text()`. The important fix is that an outer colour resumes
after an inner formatted span ends.

```python
from advancedprinter import Printer, line, strip_ansi

console = Printer()
console.print("Hello, " + line("Kaloian", color="cyan2", style="bold") + "!")
console.print("Before " + line("inside", color="cyan2") + " after", color="red1")

formatted = line("Ready for export", color="green2", style="bold")
console.print("Formatted string: " + formatted)
console.print("Plain string:     " + strip_ansi(formatted))
```

![Inline colours and restoration of outer styles](https://raw.githubusercontent.com/kbkozlev/AdvancedPrinter/083938fb4d15bb18e821719db1a0dc4c675d3a82/docs/images/inline-and-nested-styles.png)

Notice that **after** is red again. `strip_ansi()` removes formatting when you
need ordinary text. `line()` / `format_text()` return strings; they do not print.
They produce ANSI strings by default, while the eventual print operation applies
the destination policy. Use `format_text(..., color_mode="never")` to create a
plain string directly.

## 3. Frames with titles, alignment, wrapping, and preserved indentation

Frames existed before; titles, rounded borders, explicit widths, wrapping,
alignment, optional dedenting, and pure frame rendering are new. Widths are
measured in terminal cells and ignore ANSI codes, so styled text does not make
the border too long. Wide characters and combining marks are handled using
`wcwidth`; terminal-specific emoji rendering may still vary.

```python
from advancedprinter import Printer, format_frame

console = Printer()
console.frame(
    "Bitwarden   up to date\nCitrix      updated\nRambox      updated",
    title="Repository sync",
    border="rounded",
    border_color="cyan2",
    color="white",
    width=46,
)
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
console.frame(
    "A long message wraps automatically inside the chosen width.\n    Indentation is preserved.",
    title="Wrapped message",
    border="single",
    border_color="yellow1",
    width=46,
)

saved = format_frame("This frame is a string", color_mode="never")
console.print(saved)
```

![Rounded, double, wrapping, and pure string frames](https://raw.githubusercontent.com/kbkozlev/AdvancedPrinter/083938fb4d15bb18e821719db1a0dc4c675d3a82/docs/images/frames-and-wrapping.png)

`width` is the **total** width including borders and padding. Use `max_width`
for an upper limit without forcing short content to fill a larger frame.
`frame()` prints immediately; `format_frame()` returns a reusable string.
Indentation is kept unless you explicitly request `dedent=True`.

## 4. Status messages, themes, and standard logging

The new convenience methods apply consistent labels and styling. These are
particularly useful in repository updaters and other maintenance scripts.

```python
from advancedprinter import MessageStyle, Printer

console = Printer()
console.success("Repository updated")
console.info("Downloaded", 3, "packages")
console.warning("Using cached release information")
console.error("Example failure: connection timed out")

custom = Printer(
    theme={
        "success": MessageStyle("cyan2", "bold", "DONE"),
    }
)
custom.success("A custom prefix and colour")
```

![Default messages, a custom theme, and standard logging levels](https://raw.githubusercontent.com/kbkozlev/AdvancedPrinter/083938fb4d15bb18e821719db1a0dc4c675d3a82/docs/images/messages-and-logging.png)

`error()` uses stderr by default; the other methods use the printer's output
stream. The visible labels remain useful when colours are disabled. Each Printer
has its own streams, policies, and theme, so changing one does not configure the
whole application.

The lower half of the image uses Python's normal `logging` module:

```python
import logging
import sys
from advancedprinter import ColorFormatter

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColorFormatter("%(levelname)s: %(message)s", stream=handler.stream))
logger = logging.getLogger("repository-sync")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.debug("Checking local metadata")
logger.info("Repository scan complete")
logger.warning("Retrying one download")
logger.error("Example failure: download unavailable")
```

Use a normal `logging.Formatter` on file handlers. AdvancedPrinter's formatter
does not change the original record or configure your loggers for you.

## 5. Colour in terminals and clean text in files

This is the main default behaviour change: `auto` checks the actual destination.
A styled message goes to a capable terminal with colour, and to a redirected
file without escape codes. You do not need separate printing code for cron.

```python
from advancedprinter import Printer

console = Printer()  # color_mode="auto"
console.print("Repository updated", color="green2", style="bold")
with open("sync.log", "w", encoding="utf-8") as log:
    console.print("Repository updated", color="green2", style="bold", file=log)
```

![Automatic policy on a terminal versus a file destination](https://raw.githubusercontent.com/kbkozlev/AdvancedPrinter/083938fb4d15bb18e821719db1a0dc4c675d3a82/docs/images/terminal-and-log-file.png)

For a repeatable comparison, this demo uses an in-memory simulated terminal and
an in-memory non-terminal stream. Both messages are produced by the same real
`Printer.print()` method. The final `repr()` shows that the file contains only
the message and newline, with no `\x1b` escape sequences.

| Policy | Behaviour |
|---|---|
| `auto` | Detect the destination; respect non-empty `NO_COLOR`; use plain output for non-terminals or `TERM=dumb` |
| `always` | Explicitly emit ANSI styling, including when capturing screenshots |
| `never` | Produce plain output and strip embedded ANSI sequences |

`NO_COLOR` suppresses default colours, while attributes such as bold can remain.
Use `never` to turn off all styling. `color` is the text colour; `color_mode` is
the output policy. Pure formatting functions require an explicit policy and
do not accept `auto`, because they have no destination stream to inspect.

## Other improvements you will notice

- `input()` works with no prompt, preserves prompt spaces, and stringifies
  non-string prompts. You can still style it with `color` and `style`.
- `sep`, `end`, `file`, and `flush` behave like standard print parameters.
- Empty frames work; misspelled colours/styles/borders and conflicting aliases
  raise descriptive errors instead of silently hiding mistakes.
- `python -m advancedprinter` provides a built-in palette demonstration.
- The public API has type hints; CI and automated release checks cover the
  supported Python versions and operating systems.

Python 3.10+ is required. See [the API reference](api.md) and
[migration guide](migration.md) for exact compatibility details.

## Regenerate the pictures

These commands are for a source checkout, not just the PyPI installation:

```bash
python -m pip install -e '.[screenshots]'
python scripts/render_examples.py
```

The renderer uses `pyte`, Pillow, and the DejaVu Sans Mono font family. The default
font directory is `/usr/share/fonts/truetype/dejavu`; use `--font-dir` to point to
another installation containing the four font files. The generated images are
stored in `docs/images/`. Regeneration executes the examples, so the pictures
stay grounded in the actual library output. If the images change, commit them
and update the pinned image URLs in this guide and the README to the new commit.

# Contributing

Use Python 3.10 or newer. Create a virtual environment, activate it for your
platform, then install the development tools:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
```

Run the same checks used by CI:

```bash
python -m pytest --cov=advancedprinter --cov-fail-under=90
python -m ruff check .
python -m ruff format --check .
python -m mypy src/advancedprinter
python -m build
python -m twine check --strict dist/*
python -m advancedprinter
```

Use `python -m ruff format .` to format changes. Tests run against the installed
package; there is no implicit `src` path injection. Build in a clean checkout
or clear old build outputs before a release so stale versions are not included.

## Project layout

| Path | Purpose |
|---|---|
| `src/advancedprinter/styles.py` | Validated colour/style specifications and aliases |
| `src/advancedprinter/terminal.py` | ANSI handling, destination policy, Windows VT support |
| `src/advancedprinter/render.py` | Pure text/frame rendering and terminal cell widths |
| `src/advancedprinter/printer.py` | Configurable streams, input, messages, palette help |
| `src/advancedprinter/logging.py` | Standard logging formatter adapter |
| `src/advancedprinter/main.py` | Original class API compatibility |
| `src/advancedprinter/_codes.py` | Original ANSI constants |
| `tests/` | Behavioural, regression, packaging, and documentation tests |
| `examples/` | Runnable demonstrations |
| `scripts/check_release.py` | Release version/tag guard |
| `.github/workflows/` | CI and Trusted Publishing |

When changing output, test both terminal and redirected streams. For frames,
include Unicode display widths, ANSI spans, empty input, and whitespace. Keep
new runtime dependencies deliberate. See `docs/releasing.md` for publishing.

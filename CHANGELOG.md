# Changelog

## 2.0.0

### Added

- Independently configurable `Printer` instances, stream handling, and message themes.
- Readable colour/style aliases, custom hex/RGB/index colours, and depth fallback.
- Destination-aware `auto` / `always` / `never` policies, `NO_COLOR`, and Windows VT detection.
- Pure `format_text()` / `format_frame()`, ANSI stripping, and visible-width helpers.
- Success/warning/error/info helpers with visible labels; errors default to stderr.
- Unicode-aware frame wrapping, titles, padding, alignment, widths, rounded borders,
  optional dedenting, and ASCII fallback.
- Standard `logging` integration without mutating records; built-in module demo.
- Typed public API, regression tests, Linux/Windows/macOS CI, distribution checks,
  and GitHub Release-driven PyPI Trusted Publishing.

### Fixed

- Respect `sep`, and avoid unnecessary resets for unstyled text.
- Support zero-argument input; preserve prompt whitespace and stringify prompts.
- Support empty frames, preserve indentation and trailing whitespace, and measure
  terminal cells rather than ANSI bytes or code-point counts.
- Restore outer formatting after nested spans and selective resets.
- Validate unknown colours, styles, borders, and conflicting aliases.

### Changed

- Require Python 3.10+ and `wcwidth>=0.9,<1`.
- Printing uses automatic colour policy by default; redirected output is plain.
- Unknown options raise errors instead of silently falling back.
- Consolidate packaging in `pyproject.toml` and remove tracked IDE configuration.

See `docs/migration.md` for compatibility details.

## 1.2.0 — 2024-03-06

- Add styled input prompts.

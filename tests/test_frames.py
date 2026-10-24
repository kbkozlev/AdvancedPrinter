import io

import pytest

from advancedprinter import Printer, format_frame, line, strip_ansi, visible_width


def plain(text, **options):
    return format_frame(text, color_mode="never", **options)


def test_empty_frame_and_no_trailing_newline():
    assert plain("") == "+---+\n|   |\n+---+"


def test_preserves_indentation_trailing_spaces_and_blank_lines():
    rendered = plain("  code  \n\n")
    rows = rendered.splitlines()
    assert rows[1] == "|   code   |"
    assert len(rows) == 5


def test_dedent_is_opt_in():
    assert plain("  hello\n  world", dedent=True) == plain("hello\nworld")


@pytest.mark.parametrize("text", ["中文", "cafe\u0301", "👨\u200d👩\u200d👧", "🇧🇬", "a\tb"])
def test_unicode_and_tabs_are_aligned(text):
    widths = [visible_width(row) for row in plain(text + "\nx").splitlines()]
    assert len(set(widths)) == 1


def test_ansi_sequences_are_not_counted_in_width():
    rendered = format_frame(line("hi", c="red"), border="double")
    assert len({visible_width(row) for row in rendered.splitlines()}) == 1
    assert "═" * 4 in strip_ansi(rendered)


@pytest.mark.parametrize(
    "border,corner",
    [("basic", "+"), ("basic2", "="), ("single", "┌"), ("double", "╔"), ("rounded", "╭")],
)
def test_borders(border, corner):
    assert plain("x", border=border).startswith(corner)


def test_ascii_override():
    assert plain("x", border="double", ascii=True) == plain("x")


def test_legacy_positional_arguments():
    assert strip_ansi(format_frame("x", "double", "red", "blue", "white", "black", "b")) == plain(
        "x", border="double"
    )


@pytest.mark.parametrize(
    "align,body", [("left", "| x    |"), ("right", "|    x |"), ("center", "|  x   |")]
)
def test_alignment(align, body):
    assert plain("x", width=8, align=align).splitlines()[1] == body


def test_width_max_width_and_padding():
    assert all(visible_width(row) == 10 for row in plain("abcdefghi", width=10).splitlines())
    assert all(visible_width(row) <= 8 for row in plain("abcdefghijkl", max_width=8).splitlines())
    assert plain("x", padding=0) == "+-+\n|x|\n+-+"


def test_wrapping_preserves_text_and_emoji_clusters():
    text = "👨\u200d👩\u200d👧abcd"
    rendered = plain(text, width=7)
    assert rendered.count("👨\u200d👩\u200d👧") == 1
    assert all(visible_width(row) == 7 for row in rendered.splitlines())
    assert "".join(row[2:-2].rstrip() for row in rendered.splitlines()[1:-1]) == text


def test_wrapped_ansi_has_consistent_width():
    rendered = format_frame(line("abcdefghij", c="red"), width=8)
    assert all(visible_width(row) == 8 for row in rendered.splitlines())
    assert "\x1b[31m" in rendered.splitlines()[2]


def test_title():
    assert plain("hello", title="Title", width=15).splitlines()[0] == "+ Title ------+"


def test_printed_frame_and_no_color(terminal, monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    Printer(file=terminal).frame("x", c="red", s="b", border="double")
    assert "\x1b[31m" not in terminal.getvalue()
    assert "\x1b[1m" in terminal.getvalue()


def test_frame_accepts_output_controls():
    out = io.StringIO()
    Printer().frame("x", file=out, end="!")
    assert out.getvalue() == plain("x") + "!"


@pytest.mark.parametrize(
    "options",
    [
        {"border": "bad"},
        {"padding": -1},
        {"padding": True},
        {"width": 4},
        {"width": True},
        {"max_width": 1},
        {"width": 10, "max_width": 8},
        {"align": "bad"},
        {"title": "a\nb"},
        {"title": "long title", "width": 6},
        {"wrap": False, "width": 5},
        {"color_mode": "auto"},
        {"color_system": "auto"},
        {"c": "red", "color": "blue"},
        {"f_s": "single", "border": "double"},
    ],
)
def test_invalid_frame_options(options):
    with pytest.raises((TypeError, ValueError)):
        format_frame("abcdef", **options)


def test_nonprintable_control_characters_rejected():
    with pytest.raises(ValueError, match="control character"):
        plain("a\bb")


def test_wide_character_cannot_fit():
    with pytest.raises(ValueError, match="character is wider"):
        plain("中", width=5)


def test_empty_border_name_is_invalid():
    with pytest.raises(ValueError, match="Unknown border"):
        plain("x", border="")

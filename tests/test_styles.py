import pytest

from advancedprinter import format_text, line, strip_ansi
from advancedprinter.styles import BACKGROUNDS, FOREGROUNDS, color_code, style_code
from advancedprinter.terminal import strip_colors


def test_unstyled_text_and_empty_text_have_no_escape():
    assert format_text("hello") == "hello"
    assert format_text() == ""
    assert format_text(1, 2, sep="|", end="!") == "1|2!"


@pytest.mark.parametrize("name", list(FOREGROUNDS))
def test_legacy_foregrounds(name):
    assert color_code(name.upper()) == FOREGROUNDS[name]


@pytest.mark.parametrize("name", list(BACKGROUNDS))
def test_legacy_backgrounds(name):
    assert color_code(name.upper(), background=True) == BACKGROUNDS[name]


@pytest.mark.parametrize(
    "short,long",
    [
        ("b", "bold"),
        ("it", "italic"),
        ("u", "underline"),
        ("inv", "inverted"),
        ("str", "strike-through"),
    ],
)
def test_style_aliases(short, long):
    assert style_code(short) == style_code(long)


def test_styles_combine_and_deduplicate():
    assert style_code("b-it-u-b") == "\x1b[1m\x1b[3m\x1b[4m"
    assert style_code(["bold", "italic"]) == style_code("bold italic")
    assert style_code("bold,strike-through") == style_code("b-str")


def test_custom_colors_and_default():
    assert color_code("#ff0000") == color_code((255, 0, 0)) == "\x1b[38;2;255;0;0m"
    assert color_code(208, background=True) == "\x1b[48;5;208m"
    assert color_code("default") == "\x1b[39m"
    assert color_code("default", background=True) == "\x1b[49m"


def test_depth_fallback():
    assert color_code("#ff0000", system="256") == "\x1b[38;5;9m"
    assert color_code((255, 0, 0), system="standard") == "\x1b[91m"
    assert color_code(196, background=True, system="standard") == "\x1b[101m"
    assert color_code("orange", system="standard").startswith("\x1b[")


@pytest.mark.parametrize(
    "value",
    ["gren", "#fff", "#zzzzzz", -1, 256, True, (0, 1), (256, 0, 0), (True, 0, 0), [0, 0, 0], 1.2],
)
def test_invalid_colors(value):
    with pytest.raises(ValueError):
        color_code(value)


@pytest.mark.parametrize("value", ["bodl", "bold-", ["unknown"], 5])
def test_invalid_styles(value):
    with pytest.raises((ValueError, TypeError)):
        style_code(value)


def test_nested_reset_restores_outer_style():
    result = line("before " + line("inner", c="blue") + " after", c="red", s="b")
    assert "\x1b[0m\x1b[1m\x1b[31m after" in result
    assert strip_ansi(result) == "before inner after"


def test_nested_rgb_zero_channels_are_not_resets():
    result = line(line("inner", c=(255, 0, 0)), c="blue")
    assert "\x1b[38;2;255;0;0minner" in result


def test_combined_reset_keeps_following_inner_color():
    result = line("before\x1b[0;34minner", c="red")
    assert "\x1b[0m\x1b[31m\x1b[34minner" in result


@pytest.mark.parametrize(
    "reset,outer",
    [
        (39, {"c": "red"}),
        (49, {"b": "blue"}),
        (22, {"s": "b"}),
        (23, {"s": "it"}),
        (24, {"s": "u"}),
        (27, {"s": "inv"}),
        (29, {"s": "str"}),
    ],
)
def test_selective_resets_restore_outer(reset, outer):
    result = line(f"inner\x1b[{reset}m after", **outer)
    prefix = line("", **outer).removesuffix("\x1b[0m")
    assert f"\x1b[{reset}m{prefix} after" in result


def test_plain_mode_strips_inline_styles():
    assert format_text(line("hi", c="red"), color_mode="never") == "hi"


def test_no_color_removes_only_color_parameters():
    assert strip_colors("\x1b[1;38;2;255;0;0mred\x1b[0m") == "\x1b[1mred\x1b[0m"
    assert strip_colors("\x1b[48;5;208mbg\x1b[39m") == "bg"


def test_strip_ansi_handles_hyperlinks():
    assert strip_ansi("\x1b]8;;https://example.com\x1b\\link\x1b]8;;\x1b\\") == "link"


@pytest.mark.parametrize(
    "options",
    [
        {"color_mode": "auto"},
        {"color_system": "auto"},
        {"color_mode": "bad"},
        {"color_system": "bad"},
        {"end": None},
        {"b": "red", "background": "blue"},
        {"s": "b", "style": "u"},
    ],
)
def test_pure_format_validation(options):
    with pytest.raises((ValueError, TypeError)):
        format_text("x", **options)


def test_plain_formatting_also_strips_ansi_from_end():
    assert format_text("x", end=line("!", c="red"), color_mode="never") == "x!"

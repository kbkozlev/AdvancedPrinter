import builtins
import io

import pytest

import advancedprinter as ap
from advancedprinter import AdvancedPrinter, MessageStyle, Printer, format_text


@pytest.mark.parametrize("values", [(), ("hello",), ("a", "b"), (1, None, {"a": 2}), ("", "")])
@pytest.mark.parametrize("sep", [" ", "|", "", None])
@pytest.mark.parametrize("end", ["\n", "", "!", None])
def test_plain_print_matches_builtin(values, sep, end):
    expected, actual = io.StringIO(), io.StringIO()
    builtins.print(*values, sep=sep, end=end, file=expected)
    Printer().print(*values, sep=sep, end=end, file=actual)
    assert actual.getvalue() == expected.getvalue()


def test_flush_and_current_stdout(monkeypatch):
    class Flushing(io.StringIO):
        calls = 0

        def flush(self):
            self.calls += 1

    console = Printer()
    output = Flushing()
    monkeypatch.setattr("sys.stdout", output)
    console.print("ok", flush=True)
    assert output.getvalue() == "ok\n"
    assert output.calls == 1


def test_destination_policy_uses_overridden_file(terminal):
    console = Printer(file=terminal)
    plain = io.StringIO()
    console.print("red", c="red", file=plain)
    console.print("red", c="red")
    assert plain.getvalue() == "red\n"
    assert "\x1b[31m" in terminal.getvalue()


def test_never_strips_nested_ansi(terminal):
    Printer(color_mode="never", file=terminal).print(ap.line("red", c="red"))
    assert terminal.getvalue() == "red\n"


def test_always_overrides_no_color_and_nonterminal(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    out = io.StringIO()
    Printer(color_mode="always", file=out).print("red", c="red")
    assert out.getvalue() == "\x1b[31mred\x1b[0m\n"


def test_no_color_preserves_styles_and_removes_nested_colors(terminal, monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    Printer(file=terminal).print(ap.line("red", c="red"), c="blue", s="bold")
    assert "\x1b[1m" in terminal.getvalue()
    assert "\x1b[31m" not in terminal.getvalue()
    assert "\x1b[34m" not in terminal.getvalue()


def test_empty_no_color_does_not_disable_color(terminal, monkeypatch):
    monkeypatch.setenv("NO_COLOR", "")
    Printer(file=terminal).print("red", c="red")
    assert "\x1b[31m" in terminal.getvalue()


def test_dumb_terminal(terminal, monkeypatch):
    monkeypatch.setenv("TERM", "dumb")
    Printer(file=terminal).print("red", c="red", s="bold")
    assert terminal.getvalue() == "red\n"


@pytest.mark.parametrize("prompt", ["", "  prompt:  ", 123, None])
def test_input_preserves_prompt_and_returns_answer(prompt, monkeypatch):
    output = io.StringIO()
    monkeypatch.setattr("builtins.input", lambda: "answer")
    assert Printer(file=output).input(prompt) == "answer"
    assert output.getvalue() == str(prompt)


def test_input_without_prompt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: "answer")
    assert Printer(file=io.StringIO()).input() == "answer"


@pytest.mark.parametrize("error", [EOFError, KeyboardInterrupt])
def test_input_exceptions_propagate(error, monkeypatch):
    def read():
        raise error

    monkeypatch.setattr("builtins.input", read)
    with pytest.raises(error):
        Printer(file=io.StringIO()).input()


def test_input_too_many_arguments():
    with pytest.raises(TypeError):
        Printer().input("one", "two")


@pytest.mark.parametrize("interface", [ap, AdvancedPrinter, AdvancedPrinter()])
def test_legacy_interfaces(interface, capsys):
    interface.print("a", "b", sep="|")
    assert capsys.readouterr().out == "a|b\n"
    assert interface.line("red", c="red") == format_text("red", color="red")
    assert interface.C.RED == "\x1b[31m" if hasattr(interface, "C") else True


def test_instances_and_error_stream_are_independent():
    one, two, errors = io.StringIO(), io.StringIO(), io.StringIO()
    a = Printer(file=one, error_file=errors, theme={"success": MessageStyle("blue", prefix="DONE")})
    b = Printer(file=two)
    a.success("a")
    b.success("b")
    a.error("failed")
    assert one.getvalue() == "DONE a\n"
    assert two.getvalue() == "[SUCCESS] b\n"
    assert errors.getvalue() == "[ERROR] failed\n"


def test_error_defaults_to_current_stderr(capsys):
    Printer().error("failed")
    assert capsys.readouterr().err == "[ERROR] failed\n"


def test_semantic_helpers_separators_and_prefixes():
    out = io.StringIO()
    printer = Printer(file=out)
    printer.info("a", "b", sep="|", end="!")
    printer.warning()
    assert out.getvalue() == "[INFO] a|b![WARNING]\n"


@pytest.mark.parametrize(
    "options",
    [
        {"theme": {"bad": MessageStyle()}},
        {"theme": {"success": "green"}},
        {"color_mode": "bad"},
        {"color_system": "bad"},
    ],
)
def test_invalid_configuration(options):
    with pytest.raises((ValueError, TypeError)):
        Printer(**options)


@pytest.mark.parametrize(
    "options",
    [
        {"c": "red", "color": "blue"},
        {"sep": 2},
        {"end": 2},
        {"unknown": True},
        {"c": "gren"},
        {"s": "bodl"},
    ],
)
def test_print_rejects_invalid_options(options):
    with pytest.raises((TypeError, ValueError)):
        Printer(file=io.StringIO()).print("x", **options)


@pytest.mark.parametrize("method", ["print", "frame"])
def test_ansi_in_end_is_plain_when_redirected(method):
    out = io.StringIO()
    getattr(Printer(file=out), method)("hello", end=ap.line("!", c="red"))
    assert "\x1b" not in out.getvalue()
    assert out.getvalue().endswith("!")


def test_no_color_also_applies_to_end(terminal, monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    console = Printer(file=terminal)
    console.print("hi", end=ap.line("!", c="red", s="b"))
    console.frame("hi", end=ap.line("!", c="red", s="b"))
    assert "\x1b[31m" not in terminal.getvalue()
    assert "\x1b[1m" in terminal.getvalue()

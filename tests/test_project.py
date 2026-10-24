import importlib.metadata
import importlib.resources
import re
import runpy
from pathlib import Path

import pytest

import advancedprinter

ROOT = Path(__file__).resolve().parents[1]


def test_installed_metadata_and_typing_marker():
    assert advancedprinter.__version__ == importlib.metadata.version("AdvancedPrinter")
    assert importlib.resources.files("advancedprinter").joinpath("py.typed").is_file()
    assert importlib.metadata.metadata("AdvancedPrinter")["Requires-Python"] == ">=3.10"


def test_module_demo(capsys):
    runpy.run_module("advancedprinter", run_name="__main__")
    output = capsys.readouterr().out
    assert "[SUCCESS] Ready to print" in output
    assert "Text Colors:" in output
    assert "\x1b" not in output


@pytest.mark.parametrize("example", ["repository_sync.py", "styled_logging.py"])
def test_runnable_examples(example, capsys):
    runpy.run_path(str(ROOT / "examples" / example), run_name="__main__")
    captured = capsys.readouterr()
    assert captured.out or captured.err


def test_readme_python_examples_execute(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", lambda: "yes")
    namespace = {}
    for snippet in re.findall(r"```python\n(.*?)```", (ROOT / "README.md").read_text(), re.S):
        exec(compile(snippet, "README.md", "exec"), namespace)
    assert namespace["answer"] == "yes"
    assert (tmp_path / "sync.log").read_text() == "This file gets plain text\n"
    capsys.readouterr()


@pytest.mark.parametrize("tag", ["2.0.0", "v2.0.0"])
def test_release_tag_accepts_matching_version(tag):
    check = runpy.run_path(str(ROOT / "scripts" / "check_release.py"))["check_tag"]
    check(tag, "2.0.0")


@pytest.mark.parametrize("tag", ["", "v1.2.0", "v2.0", "v2.0.0rc1", "release-2.0.0"])
def test_release_tag_rejects_mismatches(tag):
    check = runpy.run_path(str(ROOT / "scripts" / "check_release.py"))["check_tag"]
    with pytest.raises(ValueError, match="does not match"):
        check(tag, "2.0.0")


def test_visual_guide_python_examples_execute(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    namespace = {}
    for snippet in re.findall(
        r"```python\n(.*?)```", (ROOT / "docs" / "visual-guide.md").read_text(), re.S
    ):
        exec(compile(snippet, "docs/visual-guide.md", "exec"), namespace)
    assert (tmp_path / "sync.log").read_text() == "Repository updated\n"
    assert namespace["saved"].startswith("+")
    capsys.readouterr()

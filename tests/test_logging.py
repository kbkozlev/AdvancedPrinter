import io
import logging

import pytest

from advancedprinter import ColorFormatter


@pytest.mark.parametrize(
    "level", [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
)
def test_color_formatter_keeps_records_and_file_handler_plain(level, terminal):
    record = logging.LogRecord("demo", level, "test.py", 1, "hello %s", ("world",), None)
    before = record.msg, record.args
    formatter = ColorFormatter("%(levelname)s: %(message)s", stream=terminal)
    styled = formatter.format(record)
    plain = logging.Formatter("%(levelname)s: %(message)s").format(record)
    assert "\x1b[" in styled
    assert "\x1b" not in plain
    assert "hello world" in plain
    assert (record.msg, record.args) == before


def test_redirected_logging_is_plain():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(ColorFormatter("%(message)s", stream=stream))
    handler.handle(logging.makeLogRecord({"msg": "test", "levelno": logging.ERROR}))
    assert stream.getvalue() == "test\n"


def test_logging_exception_traceback_is_preserved():
    try:
        raise ValueError("failure")
    except ValueError:
        import sys

        record = logging.LogRecord("demo", logging.ERROR, "test.py", 1, "oops", (), sys.exc_info())
    result = ColorFormatter(color_mode="never").format(record)
    assert "ValueError: failure" in result
    assert "\x1b" not in result


def test_logging_does_not_add_or_change_record_attributes():
    record = logging.makeLogRecord({"msg": "hello %s", "args": ("world",), "levelno": logging.INFO})
    before = dict(record.__dict__)
    ColorFormatter(color_mode="always").format(record)
    assert record.__dict__ == before

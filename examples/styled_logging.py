"""Use AdvancedPrinter with a standard logging handler."""

import logging
import sys

from advancedprinter import ColorFormatter


def main() -> None:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(ColorFormatter("%(levelname)s: %(message)s", stream=handler.stream))
    logger = logging.getLogger("advancedprinter-example")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    try:
        logger.info("Repository scan complete")
        logger.warning("Using cached metadata")
    finally:
        logger.removeHandler(handler)
        handler.close()


if __name__ == "__main__":
    main()

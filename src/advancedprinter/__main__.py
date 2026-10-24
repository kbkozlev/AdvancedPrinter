"""Run python -m advancedprinter for a destination-aware demonstration."""

from .printer import Printer


def main() -> None:
    console = Printer()
    console.frame(
        "Colours, styles, and Unicode-aware frames",
        title="AdvancedPrinter",
        border="rounded",
        max_width=60,
    )
    console.help()
    console.success("Ready to print")
    console.info("Redirect this demo to a file to get plain output.")


if __name__ == "__main__":
    main()

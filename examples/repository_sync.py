"""An example status summary for a repository updater (does not download anything)."""

from advancedprinter import MessageStyle, Printer


def main() -> None:
    console = Printer(
        theme={
            "success": MessageStyle("green2", "bold", "DONE"),
        }
    )
    console.frame(
        "Bitwarden: up to date\nCitrix: updated\nRambox: updated",
        title="Repository sync",
        border="rounded",
        max_width=50,
    )
    console.info("Checked", 3, "repositories")
    console.success("Finished")


if __name__ == "__main__":
    main()

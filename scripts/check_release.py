"""Fail a release before upload if its tag does not match installed metadata."""

from __future__ import annotations

import argparse
import os
from importlib.metadata import version


def check_tag(tag: str, package_version: str) -> None:
    if tag not in (package_version, "v" + package_version):
        raise ValueError(f"Release tag {tag!r} does not match package version {package_version!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", default=os.environ.get("RELEASE_TAG", ""))
    arguments = parser.parse_args()
    installed = version("AdvancedPrinter")
    try:
        check_tag(arguments.tag, installed)
    except ValueError as error:
        parser.error(str(error))
    print(f"Release tag matches AdvancedPrinter {installed}")


if __name__ == "__main__":
    main()

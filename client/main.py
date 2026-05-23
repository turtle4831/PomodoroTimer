"""Entry point for the PyQt6 desktop client."""

import sys

from client.app import run_app


def main() -> None:
    sys.exit(run_app())


if __name__ == "__main__":
    main()

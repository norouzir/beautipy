"""Command-line interface for BeautiPy. Enables `python -m beautipy`."""

import sys

from beautipy.cli import main

if __name__ == "__main__":
    sys.exit(main())

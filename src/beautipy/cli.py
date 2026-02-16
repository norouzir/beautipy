"""Command-line interface for BeautiPy."""

from __future__ import annotations
import argparse
import sys
from importlib.metadata import PackageNotFoundError, version

from beautipy import beautify


class CustomFormatter(
    argparse.RawDescriptionHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter
):
    pass

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_INTERRUPTED = 130

EXAMPLES = """
examples:
  beautipy '{"a": 1, "b": [2, 3]}'
  echo '[1, 2, 3]' | beautipy
  cat messy.json | beautipy -b 1 -i "  "
  beautipy -o '{"key":"value"}' > formatted.txt
"""


def _resolve_version() -> str:
    """Return the installed package version with a safe fallback."""
    try:
        return version("beautipy")
    except PackageNotFoundError:
        # Fall back to the package attribute when metadata is unavailable (e.g. in tests).
        try:
            from beautipy import __version__  # type: ignore import-not-found
        except ImportError:
            return "unknown"
        return __version__


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="beautipy",
        description="Prettify data structures into human-readable strings.",
        epilog=EXAMPLES,
        formatter_class=CustomFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {_resolve_version()}",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Input text (concatenated). If omitted, read from stdin.",
    )
    parser.add_argument(
        "-b",
        "--blank-line-depth",
        type=int,
        default=0,
        metavar="N",
        help="Number of nesting levels that receive a blank line",
    )
    parser.add_argument(
        "-s",
        "--opener-same-line",
        action="store_true",
        help="Keep opening characters on the same line",
    )
    parser.add_argument(
        "-o",
        "--compact-operators",
        action="store_true",
        help="Do not add spaces around = and :",
    )
    parser.add_argument(
        "-e",
        "--expand-empty",
        action="store_true",
        help="Expand empty structures like {} or [] onto multiple lines",
    )
    parser.add_argument(
        "-i",
        "--indent",
        default="    ",
        metavar="STR",
        help="Indentation string",
    )
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> int:
    try:
        ns = parse_args(args)
    except SystemExit as e:
        return e.code if e.code is not None else EXIT_OK

    try:
        stdin = sys.stdin
        stdin_is_tty = getattr(stdin, "isatty", lambda: False)()

        if ns.text:
            text = " ".join(ns.text)
        elif not stdin_is_tty:
            text = stdin.read()
            if text == "":
                print("beautipy: no input provided", file=sys.stderr)
                print("Try 'beautipy --help' for usage information.", file=sys.stderr)
                return EXIT_ERROR
        else:
            print("beautipy: no input provided", file=sys.stderr)
            print("Try 'beautipy --help' for usage information.", file=sys.stderr)
            return EXIT_ERROR

    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        return EXIT_INTERRUPTED
    except OSError as err:
        print(f"beautipy: read error: {err}", file=sys.stderr)
        return EXIT_ERROR
    except Exception as err:
        print(f"beautipy: unexpected error: {err}", file=sys.stderr)
        return EXIT_ERROR

    try:
        result = beautify(
            text,
            blank_line_depth=ns.blank_line_depth,
            opener_same_line=ns.opener_same_line,
            compact_operators=ns.compact_operators,
            expand_empty=ns.expand_empty,
            indent=ns.indent,
        )
    except ValueError as err:
        print(f"beautipy: {err}", file=sys.stderr)
        return EXIT_ERROR
    except Exception as err:
        print(f"beautipy: unexpected error: {err}", file=sys.stderr)
        return EXIT_ERROR

    print(result)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

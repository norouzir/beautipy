"""Pytest tests for beautipy.cli."""

from io import StringIO
from unittest.mock import patch

import pytest

from beautipy.cli import EXIT_ERROR, EXIT_OK, main, parse_args


class TestParseArgs:
    """Tests for parse_args()."""

    def test_no_args_defaults(self) -> None:
        ns = parse_args([])
        assert ns.text == []
        assert ns.blank_line_depth == 0
        assert ns.opener_same_line is False
        assert ns.compact_operators is False
        assert ns.expand_empty is False
        assert ns.indent == "    "

    def test_positional_text(self) -> None:
        ns = parse_args(["  { 'a': 1 }  "])
        assert ns.text == ["  { 'a': 1 }  "]

    def test_positional_text_multiple_joined(self) -> None:
        ns = parse_args(["{}", "and", "[]"])
        assert ns.text == ["{}", "and", "[]"]

    def test_blank_line_depth(self) -> None:
        ns = parse_args(["-b", "2"])
        assert ns.blank_line_depth == 2
        ns = parse_args(["--blank-line-depth", "1"])
        assert ns.blank_line_depth == 1

    def test_opener_same_line(self) -> None:
        ns = parse_args(["-s"])
        assert ns.opener_same_line is True
        ns = parse_args(["--opener-same-line"])
        assert ns.opener_same_line is True

    def test_compact_operators(self) -> None:
        ns = parse_args(["-o"])
        assert ns.compact_operators is True
        ns = parse_args(["--compact-operators"])
        assert ns.compact_operators is True

    def test_expand_empty(self) -> None:
        ns = parse_args(["-e"])
        assert ns.expand_empty is True
        ns = parse_args(["--expand-empty"])
        assert ns.expand_empty is True

    def test_indent(self) -> None:
        ns = parse_args(["-i", "\t"])
        assert ns.indent == "\t"
        ns = parse_args(["--indent", "  "])
        assert ns.indent == "  "

    def test_combined_flags(self) -> None:
        ns = parse_args(["-e", "-o", "-b", "1", "{}"])
        assert ns.expand_empty is True
        assert ns.compact_operators is True
        assert ns.blank_line_depth == 1
        assert ns.text == ["{}"]


class TestMain:
    """Tests for main() with passed args (no stdin)."""

    def test_main_with_positional_input(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        code = main(["{'a': 1}"])
        out, err = capsys.readouterr()
        assert code == EXIT_OK
        assert "'a'" in out
        assert "1" in out
        assert err == ""

    def test_main_with_stdin_when_no_args(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        with patch("sys.stdin", StringIO('{"x": 1}')):
            code = main([])
        out, err = capsys.readouterr()
        assert code == EXIT_OK
        assert '"x"' in out
        assert "1" in out
        assert err == ""

    def test_main_expand_empty(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = main(["-e", "{}"])
        out, err = capsys.readouterr()
        assert code == EXIT_OK
        assert "{" in out
        assert "}" in out
        assert out.strip() != "{}"
        assert err == ""

    def test_main_compact_operators(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = main(["-o", '{"a": 1}'])
        out, err = capsys.readouterr()
        assert code == EXIT_OK
        assert ":1" in out and "a" in out  # no space before 1 (compact)
        assert err == ""

    def test_main_opener_same_line(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = main(["-s", '{"a": 1}'])
        out, err = capsys.readouterr()
        assert code == EXIT_OK
        assert "{" in out and "a" in out
        assert err == ""

    def test_main_custom_indent(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = main(["--indent", "  ", '{"a": 1}'])
        out, err = capsys.readouterr()
        assert code == EXIT_OK
        assert "  " in out
        assert err == ""

    def test_main_blank_line_depth(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = main(["-b", "0", '{"a": 1}'])
        out, err = capsys.readouterr()
        assert code == EXIT_OK
        assert "a" in out and "1" in out
        assert err == ""

    def test_main_multiple_positional_joined(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        code = main(["{}", "  ", "[]"])
        out, err = capsys.readouterr()
        assert code == EXIT_OK
        # Input is "{}   []" -> parsed and beautified
        assert "{" in out or "[" in out
        assert err == ""

    def test_main_returns_error_when_no_input(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        with patch("sys.stdin", StringIO("")):
            code = main([])
        _, err = capsys.readouterr()
        assert code == EXIT_ERROR
        assert "no input" in err

    def test_main_returns_error_when_no_input_tty(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        class FakeTTY:
            def isatty(self) -> bool:
                return True

            def read(self) -> str:
                return ""

        with patch("sys.stdin", FakeTTY()):
            code = main([])
        _, err = capsys.readouterr()
        assert code == EXIT_ERROR
        assert "no input" in err

    def test_main_returns_error_on_value_error(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        code = main(["-b", "-1", "{}"])
        _, err = capsys.readouterr()
        assert code == EXIT_ERROR
        assert "blank_line_depth" in err

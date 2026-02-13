"""Pytest tests for beautipy.core."""

import pytest

from beautipy import beautify


def test_dict_basic() -> None:
    result = beautify({"Mango": 2, "Cherry": 5})
    assert "'Mango': 2" in result
    assert "'Cherry': 5" in result
    assert "{" in result
    assert "}" in result


def test_list_basic() -> None:
    result = beautify([1, 2, 3])
    assert "1," in result
    assert "2," in result
    assert "3" in result


def test_nested_structure() -> None:
    data = {"a": [1, 2], "b": {"x": 10}}
    result = beautify(data)
    assert "'a':" in result
    assert "[" in result
    assert "'b':" in result
    assert "'x': 10" in result


def test_empty_dict_default() -> None:
    result = beautify({})
    assert result == "{}"


def test_empty_dict_expand_empty() -> None:
    result = beautify({}, expand_empty=True)
    assert "{" in result
    assert "}" in result
    assert result != "{}"


def test_empty_list_expand_empty() -> None:
    result = beautify([], expand_empty=True)
    assert "[" in result
    assert "]" in result
    assert result != "[]"


def test_space_around_operators_false() -> None:
    result = beautify({"a": 1}, space_around_operators=False)
    assert "'a':1" in result


def test_space_around_operators_true() -> None:
    result = beautify({"a": 1}, space_around_operators=True)
    assert "'a': 1" in result


def test_custom_indent() -> None:
    result = beautify({"a": 1}, indent="  ")
    assert "  " in result


def test_non_standard_text() -> None:
    data = 'User(id:123,name:"John",roles:{})'
    result = beautify(data)
    assert "id: 123" in result
    assert "roles:" in result


def test_string_input() -> None:
    result = beautify('{"x":1}')
    assert '"x": 1' in result


def test_extra_newline_depth_raises_on_negative() -> None:
    with pytest.raises(ValueError, match="extra_newline_depth"):
        beautify({}, extra_newline_depth=-1)


def test_quoted_strings_preserved() -> None:
    result = beautify('{"key": "value with spaces"}')
    assert "value with spaces" in result


def test_tuple_formatting() -> None:
    result = beautify((1, 2, 3))
    assert "1," in result
    assert "2," in result
    assert "3" in result


def test_opener_on_next_line_false() -> None:
    result = beautify({"a": 1}, opener_on_next_line=False)
    assert result.startswith("{") or "'a'" in result


def test_deeply_nested() -> None:
    data = {"a": {"b": {"c": [1, 2, 3]}}}
    result = beautify(data)
    assert "'c':" in result
    assert "1," in result


def test_empty_string_input() -> None:
    result = beautify("")
    assert result == ""


def test_single_closer() -> None:
    result = beautify("]")
    assert result.strip() == "]"


def test_single_opener_empty_not_expanded() -> None:
    result = beautify("{}")
    assert result == "{}"


def test_custom_indent_multichar() -> None:
    result = beautify({"a": 1}, indent="|   ")
    assert "|   " in result
    assert "'a'" in result


def test_empty_indent() -> None:
    result = beautify({"a": 1}, indent="")
    assert "'a'" in result
    assert "1" in result

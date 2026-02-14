# BeautiPy

[![PyPI version](https://img.shields.io/pypi/v/beautipy.svg)](https://pypi.org/project/beautipy/)
[![Python Versions](https://img.shields.io/pypi/pyversions/beautipy.svg)](https://pypi.org/project/beautipy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight pretty-printer for complex, nested data structures and structured text.
Improves readability by adding indentation and line breaks.

## Features

- Works with any object via its `str()` representation
- Handles non-standard structured text
- Configurable indentation and formatting rules
- Simple and dependency-free
- Includes a CLI tool

## Installation

```bash
pip install beautipy
```

Or using `uv`:

```bash
uv add beautipy
```

Requires Python 3.8 or higher.

## Quick Start

### Python

```python
from beautipy import beautify

data = {'method': 'GET', 'status': 200}
print(beautify(data))
```

Output:

```
{
    'method': 'GET',
    'status': 200
}
```

### Terminal

```bash
cat data.txt | beautipy > formatted.txt
```

You can also run as a module: `python -m beautipy`.

## Usage

### Python API

The core functionality is provided by the `beautify` function.

```python
from beautipy import beautify

beautify(
    obj: object,
    *,
    blank_line_depth: int = 0,
    opener_same_line: bool = False,
    compact_operators: bool = False,
    expand_empty: bool = False,
    indent: str = '    '
) -> str
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `obj` | `object` | - | Object to format. If not a string, `str(obj)` is used. |
| `blank_line_depth` | `int` | `0` | Number of initial nesting levels that get a blank line. |
| `opener_same_line` | `bool` | `False` | Keep `{`, `[`, `(` on the same line. |
| `compact_operators` | `bool` | `False` | Omit spaces around `=` and `:`. |
| `expand_empty` | `bool` | `False` | Expand empty structures (e.g. `{}`) to multiple lines. |
| `indent` | `str` | `'    '` | Indentation string (4 spaces by default). |

**Raises:** `ValueError` if `blank_line_depth < 0`.

### Command Line

BeautiPy can also be used directly from the terminal.

```bash
# From file
beautipy < messy.json

# From stdin
echo '[1,2,3]' | beautipy

# From argument
beautipy '{"key":"value"}'

# Multiple options
beautipy --indent '  ' -s '{key:value}'
```

#### Options

- `-b`, `--blank-line-depth N`: Add blank lines at depth N. Default is `0`.
- `-s`, `--opener-same-line`: Keep opening brackets inline.
- `-o`, `--compact-operators`: Do not add spaces around `=` and `:`.
- `-e`, `--expand-empty`: Expand empty structures (e.g. `[]`).
- `-i`, `--indent STR`: Set indentation string. Default is `'    '` (4 spaces).
- `--version`: Show version information.

## Non-standard Structured Text

Since BeautiPy operates on text rather than parsing, it can format custom structured text and does not require valid JSON, Python, or any specific syntax:

```python
text = 'Arya[age:9,parents:("mother"="Tara",father:Bardia),children:{}]'
print(beautify(text))
```

Output:

```
Arya
[
    age: 9,
    parents: 
    (
        "mother" = "Tara",
        father: Bardia
    ),
    children: {}
]
```

More usage examples can be found in the [examples/](examples/) directory:

- [txt/](examples/txt/)
- [json/](examples/json/)
- [options.py](examples/options.py)

## How It Works

BeautiPy operates purely at the character level:

1. Reads input as text
2. Identifies structural characters: `{`, `[`, `(`, `,`, etc.
3. Applies formatting rules (indentation, spacing, newlines)

This allows reasonable output for custom or made-up syntax.

## Notes

- **Not a parser**: Cannot extract or modify data — no semantic understanding
- **Not a validator**: Does not check syntactic correctness

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git switch -c feature/amazing-feature` or `git checkout -b feature/amazing-feature`)
3. Install the package in development mode with dev dependencies:
   - `pip install -e ".[dev]"` or `uv sync --extra dev`
4. Run tests: `pytest` (from the project root)
5. Submit a pull request

Please ensure:

- Code follows PEP 8
- Changes are well-documented

## License

MIT License — free to use, modify, and distribute.
See the [LICENSE](LICENSE) file for details.

## Links

- **PyPI**: https://pypi.org/project/beautipy/
- **GitHub**: https://github.com/norouzir/beautipy
- **Issues**: https://github.com/norouzir/beautipy/issues
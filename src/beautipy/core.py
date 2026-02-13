"""Core formatting logic."""

_OPENERS = {'{', '[', '('}
_CLOSERS = {'}', ']', ')'}
_QUOTES = {"'", '"'}


def beautify(
    obj: object,
    *,
    blank_line_depth: int = 0,
    opener_same_line: bool = False,
    compact_operators: bool = False,
    expand_empty: bool = False,
    indent: str = '    '
) -> str:
    """Format a data structure into a human-readable string.

    Prettifies the `str()` representation of an object by applying indentation,
    line breaks, and spacing rules, making deeply nested structures easier to
    read and understand.

    Args:
        obj: The object to format. If not a string, `str(obj)` is used internally.
        blank_line_depth: Number of nesting levels that receive a blank line.
            Must be `>= 0`. Defaults to `0`.
        opener_same_line: If True, opening characters (`{`, `[`, `(`)
            stay on the same line. Defaults to `False`.
        compact_operators: If True, no spaces around `=` and `:`
            (e.g., `key=value` instead of `key = value`). Defaults to `False`.
        expand_empty: If True, empty structures like `{}`
            or `[]` are expanded into multiple lines. Defaults to `False`.
        indent: String used for each level of indentation.
            Defaults to `    ` (4 spaces).

    Returns:
        The formatted string representation of the input object.

    Raises:
        ValueError: If `blank_line_depth` is negative.

    Examples:
        >>> data = ['Mango','Cherry']
        >>> print(beautify(data))
        [
            'Mango',
            'Cherry'
        ]
        >>> # non-standard structured text (see Notes)
        >>> data = 'Error: {code:500,msg:"Not found"}'
        >>> print(beautify(data, opener_same_line=True))
        Error: {
            code: 500,
            msg: "Not found"
        }

    Notes:
        This function is not a parser or validator and does not check
        syntactic correctness of the input or output.
        Formatting is applied purely at the textual level, based on characters,
        without semantic understanding of the input structure.
        As a result, the function can produce reasonable output even for
        non-standard or malformed syntax (see Examples).
    """

    def newline(count=0):
        count = count if count else 2 if indent_level < blank_line_depth else 1
        return count * ('\n' + indent_level * indent)

    if blank_line_depth < 0:
        raise ValueError('blank_line_depth must be greater than or equal to 0')

    indent_level = 0
    string_opener = None
    last_was_escape = False
    buffer = []
    source_text = obj if isinstance(obj, str) else str(obj)
    i = -1
    
    while i < len(source_text) - 1:
        i += 1
        char = source_text[i]

        if string_opener:
            buffer.append(char)
            if last_was_escape:
                last_was_escape = False
                continue
            if char == '\\':
                last_was_escape = True
            elif char == string_opener:
                string_opener = None
            continue
        
        if char.isspace():
            continue

        if char in _OPENERS:
            next_char = None
            next_index = i
            for j in range(i + 1, len(source_text)):
                if not source_text[j].isspace():
                    next_char = source_text[j]
                    next_index = j
                    break
            if next_char in _CLOSERS:
                if expand_empty:
                    if not opener_same_line and buffer and not buffer[-1].endswith(indent):
                        buffer.append(newline(1))
                    buffer.append(char + newline() + next_char)
                else:
                    buffer.append(char + next_char)
                i = next_index
            else:
                if not opener_same_line and buffer and not buffer[-1].endswith(indent):
                    buffer.append(newline(1))
                indent_level += 1
                buffer.append((char + newline()))
            continue
            
        if char == ',':
            buffer.append(char + newline())
            continue
        
        if char in _CLOSERS:
            buffer.append(newline())
            if buffer and buffer[-1].endswith(indent):
                buffer[-1] = buffer[-1][:-len(indent)]
            indent_level = max(indent_level - 1, 0)
            buffer.append(char)
            continue
        
        if char == '=' and not compact_operators:
            buffer.append(' = ')
            continue
        
        if char == ':' and not compact_operators:
            buffer.append(': ')
            continue
        
        if char in _QUOTES:
            string_opener = char
            buffer.append(char)
            continue

        buffer.append(char)
    
    return ''.join(buffer)

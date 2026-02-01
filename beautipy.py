def beautify(
    obj,
    *,
    extra_newline_depth: int = 0,
    opener_on_next_line: bool = True,
    space_around_operators: bool = True,
    expand_empty: bool = False,
    indent: str = '    '
) -> str:

    def newline(count=0):
        count = count if count else 2 if indent_level<extra_newline_depth else 1
        return count * ('\n' + indent_level * indent)

    if extra_newline_depth < 0:
        raise ValueError('extra_newline_depth must be equal or greater than 0')
    
    OPENERS = {'{', '[', '('}
    CLOSERS = {'}', ']', ')'}
    QUOTES = {"'", '"'}
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

        if char in OPENERS:
            next_char = None
            next_index = i
            for j in range(i + 1, len(source_text)):
                if not source_text[j].isspace():
                    next_char = source_text[j]
                    next_index = j
                    break
            if next_char in CLOSERS:
                if expand_empty:
                    if opener_on_next_line and buffer and not buffer[-1].endswith(indent):
                        buffer.append(newline(1))
                    buffer.append(char + newline() + next_char)
                else:
                    buffer.append(char + next_char)
                i = next_index
            else:
                if opener_on_next_line and buffer and not buffer[-1].endswith(indent):
                    buffer.append(newline(1))
                indent_level += 1
                buffer.append((char + newline()))
            continue
            
        if char == ',':
            buffer.append(char + newline())
            continue
        
        if char in CLOSERS:
            buffer.append(newline())
            buffer[-1] = buffer[-1].removesuffix(indent)
            indent_level = max(indent_level - 1, 0)
            buffer.append(char)
            continue
        
        if char == '=' and space_around_operators:
            buffer.append(' = ')
            continue
        
        if char == ':' and space_around_operators:
            buffer.append(': ')
            continue
        
        if char in QUOTES:
            string_opener = char
            buffer.append(char)
            continue

        buffer.append(char)
    
    return ''.join(buffer)
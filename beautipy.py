def format_structure(
    source_object,
    extra_line_depth: int = 0,
    opener_in_next_line: bool = True,
    add_space_to_assignments: bool = True,
    expand_empty_objects: bool = False,
    indent_string: str = '    '
) -> str:

    def newline(count=0):
        count = count if count else 2 if indent_level<extra_line_depth else 1
        return count * ('\n' + indent_level * indent_string)

    if extra_line_depth < 0:
        raise ValueError('extra_line_depth must be equal or greater than 0')
    
    OPENERS = {'{', '[', '('}
    CLOSERS = {'}', ']', ')'}
    QUOTES = {"'", '"'}
    indent_level = 0
    string_opener = None
    last_was_escape = False
    buffer = []
    source_text = source_object if isinstance(source_object, str) else str(source_object)
    i = -1
    
    while i < len(source_text)-1:
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
                if expand_empty_objects:
                    if opener_in_next_line and buffer and not buffer[-1].endswith(indent_string):
                        buffer.append(newline(1))
                    buffer.append(char + newline() + next_char)
                else:
                    buffer.append(char + next_char)
                i = next_index
            else:
                if opener_in_next_line and buffer and not buffer[-1].endswith(indent_string):
                    buffer.append(newline(1))
                indent_level += 1
                buffer.append((char + newline()))
            continue
            
        if char == ',':
            buffer.append(char + newline())
            continue
        
        if char in CLOSERS:
            buffer.append(newline())
            buffer[-1] = buffer[-1].removesuffix(indent_string)
            indent_level = max(indent_level - 1, 0)
            buffer.append(char)
            continue
        
        if char == '=' and add_space_to_assignments:
            buffer.append(' = ')
            continue
        
        if char == ':' and add_space_to_assignments:
            buffer.append(': ')
            continue
        
        if char in QUOTES:
            string_opener = char
            buffer.append(char)
            continue

        buffer.append(char)
    
    return ''.join(buffer)
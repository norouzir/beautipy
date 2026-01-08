def format_structure(
    source,
    extra_line_depth: int = 0,
    opener_in_next_line: bool = True,
    add_space_to_assignments: bool = True,
    expand_empty_objects: bool = False,
    indent: str = '\t'
) -> str:

    def newline(count=0):
        count = count if count else 2 if indent_level<extra_line_depth else 1
        return count * ('\n' + indent_level * indent)

    if extra_line_depth < 0:
        raise ValueError('extra_line_depth must be equal or greater than 0')
    
    OPENERS = {'{', '[', '(', '<'}
    CLOSERS = {'}', ']', ')', '>'}
    QUOTES = {"'", '"'}
    indent_level = 0
    string_opener = None
    last_was_newline = False
    buffer = []
    source_text = source if isinstance(source, str) else str(source)

    for char in source_text:

        if string_opener:
            buffer.append(char)
            if char==string_opener and buffer[-1][-1]!='\\':
                string_opener = None
        
        elif char.isspace():
            continue

        elif char in OPENERS:
            if opener_in_next_line and buffer and not last_was_newline:
                buffer.append(newline(1))
            indent_level += 1
            buffer.extend((char, newline()))
            last_was_newline = True
            
        elif char == ',':
            buffer.append(char + newline())
            last_was_newline = True
        
        elif char == '=' and add_space_to_assignments:
            buffer.append(' = ')
            last_was_newline = False
        
        elif char == ':' and add_space_to_assignments:
            buffer.append(': ')
            last_was_newline = False
        
        else:
            if char in CLOSERS:
                if last_was_newline:
                    del buffer[-1]
                    if expand_empty_objects:
                        indent_level = max(indent_level - 1, 0)
                        buffer.append(newline())
                    else:
                        del buffer[-2]
                        indent_level = max(indent_level - 1, 0)
                else:
                    buffer.append(newline())
                    buffer[-1] = buffer[-1].removesuffix(indent)
                    indent_level = max(indent_level - 1, 0)

            elif char in QUOTES:
                string_opener = char
            
            buffer.append(char)
            last_was_newline = False
    
    return ''.join(buffer)
"""Basic BeautiPy usage for structured text."""

from beautipy import beautify


def main() -> None:
    """Format a structured text."""

    # Read input structured text
    with open("input.txt", "r", encoding="utf-8") as file:
        input_text = file.read()

    # Format it
    result = beautify(input_text, blank_line_depth=3)

    # Write output
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(result)

    print("Formatting completed successfully.")
    print("Formatted text saved to 'output.txt'.")

    # Expected output: see output.txt


if __name__ == "__main__":
    main()

"""Basic BeautiPy usage for JSON text."""

from beautipy import beautify


def main() -> None:
    """Format a JSON text using default settings."""

    # Read input JSON text
    with open("input.json", "r", encoding="utf-8") as file:
        input_text = file.read()

    # Format it
    result = beautify(input_text)

    # Write output
    with open("output.json", "w", encoding="utf-8") as file:
        file.write(result)

    print("Formatting completed successfully.")
    print("Formatted text saved to 'output.json'.")

    # Expected output: see output.json


if __name__ == "__main__":
    main()

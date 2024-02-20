# AdvancedPrinter

AdvancedPrinter is a custom Python library designed to mimic the behavior of the `print` function with added color and style options using ANSI escape codes. This allows you to print text with various colors and styles to the terminal.

## Features

- Print text in different colors: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, and `orange`.
- Apply styles to text: `bold` = `b`, `italic` = `it`, and `underline` = `u`.
- Combine styles: `b-it`, `b-u`, `it-u`, and `b-it-u`.

## Usage

1. Install the package from PyPi
   ```bash
   pip install AdvancedPrinter
   ```
2. Import the `AdvancedPrinter` class into your Python script.
   
   ```python
    from advancedprinter import AdvancedPrinter as ap
   ```

3. Use the `ap.print()` method to print colored text.

   ```python
   # Example usage
   ap.print("Green text", c="green")
   ap.print("Underlined text", s="u")
   ap.print("Bold italic text", s="b-it")
   ap.print("Orange italic underlined", s="it-u", c='orange')
   ap.print("White text on blue b!", c="white", b="blue")
   ap.print("Bold red underlined italic text!", c="red", s="b-it-u")
   
   # Additional arguments example
   ap.print("This is a bold example with additional arguments.", s="b", end="***")
   ```
   ![Example1](https://i.imgur.com/sLSRK2N.png)

4. Use `ap.line()` method to print multiple colors in line using nested `f-strings`

   ```python
   name = "Kaloian"
   print(f"""{ap.line("Hello, my name is", c='green', s='b')} {ap.line(f"{name}", c='blue')} {ap.line("and I'm", c='white')} {ap.line("28", c='red')} {ap.line('years old!', c='magenta')}""", end='***')
   ```
   ![Example2](https://i.imgur.com/E7lAGM6.png)

## Optionally

1. Import `print` and `line` directly to override the inbuilt methods
   
   ```python
   from advancedprinter import print, line
   
   print("Green text", c="green")
   
   name = "Kaloian"
   print(f"""{line("Hello, my name is", c='green', s='b')} {line(f"{name}", c='blue')} {line("and I'm", c='white')} {line("28", c='red')} {line('years old!', c='magenta')}""", end='***')
   ```
   ![Example3](https://i.imgur.com/ONPWHJj.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support Me
<div>
<a href="https://www.buymeacoffee.com/kbkozlev" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</div>
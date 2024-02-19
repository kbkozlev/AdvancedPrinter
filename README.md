# AdvancedPrinter

AdvancedPrinter is a custom Python library designed to mimic the behavior of the `print` function with added color and style options using ANSI escape codes. This allows you to print text with various colors and styles to the terminal.

## Features

- Print text in different colors: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, and `orange`.
- Apply styles to text: `bold`, `italic`, and `underline`.
- Combine styles: `bold-italic`, `bold-underline`, `italic-underline`, and `bold-italic-underline`.

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
   ap.print("Green text", foreground="green")
   ap.print("Underlined text", style="underline")
   ap.print("Bold italic text", style="bold-italic")
   ap.print("Orange italic underlined", style="italic-underline", foreground='orange')
   ap.print("White text on blue background!", foreground="white", background="blue")
   ap.print("Bold red underlined italic text!", foreground="red", style="bold-italic-underline")
   
   # Additional arguments example
   ap.print("This is a bold example with additional arguments.", style="bold", end="***")
   ```
   ![Example1](https://i.imgur.com/sLSRK2N.png)

4. Use `ap.line()` method to print multiple colors in line using nested `f-strings`

   ```python
   name = "Kaloian"
   print(f"""{ap.line("Hello, my name is", foreground='green', style='bold')} {ap.line(f"{name}", foreground='blue')} {ap.line("and I'm", foreground='white')} {ap.line("28", foreground='red')} {ap.line('years old!', foreground='magenta')}""", end='***')
   ```
   ![Example2](https://i.imgur.com/E7lAGM6.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support Me
<div>
<a href="https://www.buymeacoffee.com/kbkozlev" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</div>
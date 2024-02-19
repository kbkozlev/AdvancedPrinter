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
    from advancedprinter import AdvancedPrinter as AP
   ```

3. Use the `AP.print()` method to print colored text.

   ```python
   # Example usage
   AP.print("Green text", foreground="green")
   AP.print("Underlined text", style="underline")
   AP.print("Bold italic text", style="bold-italic")
   AP.print("Orange italic underlined", style="italic-underline", foreground='orange')
   AP.print("White text on blue background!", foreground="white", background="blue")
   AP.print("Bold red underlined italic text!", foreground="red", style="bold-italic-underline")
   
   # Additional arguments example
   AP.print("This is a bold example with additional arguments.", style="bold", end="***")
   ```
   ![Example1](https://i.imgur.com/sLSRK2N.png)

4. Use `AP.line()` method to print multiple colors in line using nested `f-strings`

   ```python
   name = "Kaloian"
   print(f"""{AP.line("Hello, my name is", foreground='green', style='bold')} {AP.line(f"{name}", foreground='blue')} {AP.line("and I'm", foreground='white')} {AP.line("28", foreground='red')} {AP.line('years old!', foreground='magenta')}""", end='***')
   ```
   ![Example2](https://i.imgur.com/E7lAGM6.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

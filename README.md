# AdvancedPrinter

AdvancedPrinter is a custom Python library designed to mimic the behavior of the `print` function with added color and style options using ANSI escape codes. This allows you to print text with various colors and styles to the terminal.

## Features

- Print text in different colors: black, red, green, yellow, blue, magenta, cyan, white, and orange.
- Apply styles to text: bold, italic, and underline.
- Customize background colors: bg_black, bg_red, bg_green, bg_yellow, bg_blue, bg_magenta, bg_cyan, bg_white, and bg_orange.
- Combine multiple styles: bold-italic, bold-underline, italic-underline, and bold-italic-underline.

## Usage

1. Install the package from PyPi
   ```
   pip install AdvancedPrinter
   ```
2. Import the `AdvancedPrinter` class into your Python script.
   
    ```python
    from advancedprinter import AdvancedPrinter as AP
    ```

2. Use the `AdvancedPrint.print()` method to print colored text.

    ```python
    # Example usage
   AP.print("Hello, colored world!", foreground="green")
   AP.print("Hello, bold red underlined italic text!", foreground="red", style="bold-italic-underline")
   AP.print("Hello, black text on blue background!", foreground="black", background="blue")
   AP.print("underline", style="underline")
   AP.print("bold-italic", style="bold-italic")
   AP.print("orange bold-italic", style="bold-italic", foreground='orange')
   AP.print("Hello, black text on white background!", foreground="black", background="white")
   
   # Additional arguments example
   AP.print("This is an example with additional arguments.", style="bold", end="***")
   
   # Example usage with different colors for different parts of the string
   name_color = 'GREEN'
   age_color = 'RED'
   style = 'BOLD'
   name = "Kaloian"
   age = 30
   
   AP.print(f"\nHello, my name is ", foreground=name_color, style=style, end="")
   AP.print(f"{name}", foreground='blue', style=style, end="")
   AP.print(f" and I am ", foreground='white', style=style, end="")
   AP.print(f"{age}", foreground=age_color, style=style, end="")
   AP.print(" years old!", foreground='magenta', style=style)
    ```
   ![Example](https://i.imgur.com/fiiMm62.png)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

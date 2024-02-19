# ColorPrinter

ColorPrinter is a custom Python library designed to mimic the behavior of the `print` function with added color and style options using ANSI escape codes. This allows you to print text with various colors and styles to the terminal.

## Features

- Print text in different colors: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, and ORANGE.
- Apply styles to text: BOLD, ITALIC, and UNDERLINE.
- Customize background colors: BG_BLACK, BG_RED, BG_GREEN, BG_YELLOW, BG_BLUE, BG_MAGENTA, BG_CYAN, BG_WHITE, and BG_ORANGE.
- Combine multiple styles: BOLD-ITALIC, BOLD-UNDERLINE, ITALIC-UNDERLINE, and BOLD-ITALIC-UNDERLINE.

## Usage

1. Import the `ColorPrinter` class into your Python script.
   
    ```python
    from colorprinter import ColorPrinter
    ```

2. Use the `ColorPrint.print()` method to print colored text.

    ```python
    # Example usage
   ColorPrinter.print("Hello, colored world!", foreground="green")
   ColorPrinter.print("Hello, bold red underlined italic text!", foreground="red", style="bold-italic-underline")
   ColorPrinter.print("Hello, black text on blue background!", foreground="black", background="blue")
   ColorPrinter.print("underline", style="underline")
   ColorPrinter.print("bold-italic", style="bold-italic")
   ColorPrinter.print("orange bold-italic", style="bold-italic", foreground='orange')
   ColorPrinter.print("Hello, black text on white background!", foreground="black", background="white")
   
   # Additional arguments example
   ColorPrinter.print("This is an example with additional arguments.", style="bold", end="***")
   
   # Example usage with different colors for different parts of the string
   name_color = 'GREEN'
   age_color = 'RED'
   style = 'BOLD'
   name = "Kaloian"
   age = 30
   
   ColorPrinter.print(f"\nHello, my name is ", foreground=name_color, style=style, end="")
   ColorPrinter.print(f"{name}", foreground='blue', style=style, end="")
   ColorPrinter.print(f" and I am ", foreground='white', style=style, end="")
   ColorPrinter.print(f"{age}", foreground=age_color, style=style, end="")
   ColorPrinter.print(" years old!", foreground='magenta', style=style)
    ```
   ## Try it Online
   

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

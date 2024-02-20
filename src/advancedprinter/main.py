class AdvancedPrinter:
    """
    Custom class to mimic the behavior of the print function with added color and s options.

    Available colors:
    - BLACK
    - RED
    - GREEN
    - YELLOW
    - BLUE
    - MAGENTA
    - CYAN
    - WHITE
    - ORANGE

    Available styles:
    - BOLD
    - ITALIC
    - UNDERLINE
    - BOLD-ITALIC
    - BOLD-UNDERLINE
    - ITALIC-UNDERLINE
    - BOLD-ITALIC-UNDERLINE
    """

    class C:
        """
        Nested class containing ANSI escape codes for different text colors and styles.
        """
        RESET = '\033[0m'
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[97m'
        ORANGE = '\033[38;5;208m'

        # Background Colors
        BG_BLACK = '\033[48;5;0m'
        BG_RED = '\033[48;5;1m'
        BG_GREEN = '\033[48;5;2m'
        BG_YELLOW = '\033[48;5;3m'
        BG_BLUE = '\033[48;5;4m'
        BG_MAGENTA = '\033[48;5;5m'
        BG_CYAN = '\033[48;5;6m'
        BG_WHITE = '\033[107m'
        BG_ORANGE = '\033[48;5;208m'

        # Styles
        B = '\033[1m'
        IT = '\x1B[3m'
        U = '\x1B[4m'

    @staticmethod
    def _prepare_text(*args, foreground=None, background=None, style=None):
        """
        Helper method to prepare the colored and styled text.

        :param args: The text to print.
        :param foreground: The text color.
        :param background: The background color.
        :param style: The style.
        :return: The colored and styled text.
        """
        color_code = getattr(AdvancedPrinter.C, foreground.upper(), '') if foreground else ''
        background_code = getattr(AdvancedPrinter.C, f"BG_{background.upper()}", '') if background else ''

        # Process s
        style_code = ''
        if style:
            styles = style.split('-')
            for style in styles:
                style_code += getattr(AdvancedPrinter.C, style.upper(), '')

        text = ' '.join(str(arg) for arg in args)
        return f'{background_code}{style_code}{color_code}{text}{AdvancedPrinter.C.RESET}'

    @staticmethod
    def print(*args, c=None, b=None, s=None, end='\n', flush=False, file=None, **kwargs):
        """
        Print function wrapper with added color and style options.

        :param args: The text to print.
        :param c: The text color
        :param b: The background color.
        :param s: The style.
        :param end: The string appended after the last value, default is a newline.
        :param flush: Whether to forcibly flush the stream, default is False.
        :param file: A file-like object (stream); defaults to the current sys.stdout.
        :param kwargs: Additional keyword arguments supported by the built-in print function.
        """
        colored_text = AdvancedPrinter._prepare_text(*args, foreground=c, background=b, style=s)
        print(colored_text, end=end, flush=flush, file=file, **kwargs)

    @staticmethod
    def line(*args, c=None, b=None, s=None, end='') -> str:
        """
        Custom function with added color and style options used for inline printing

        :param args: The text to return.
        :param c: The text color.
        :param b: The background color.
        :param s: The style.
        :param end: The string appended after the last value, default is ''.
        """
        colored_text = AdvancedPrinter._prepare_text(*args, foreground=c, background=b, style=s)
        return f"{colored_text}{end}"

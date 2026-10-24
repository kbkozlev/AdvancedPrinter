"""Legacy ANSI constants, retained for AdvancedPrinter.C compatibility."""


class Codes:
    """
    Nested class containing ANSI escape codes for different text colors and styles.
    """

    RESET = "\033[0m"

    BLACK = "\033[30m"
    WHITE = "\033[97m"

    RED = "\033[31m"
    RED1 = "\033[91m"
    RED2 = "\033[38;2;128;0;0m"

    GREEN = "\033[38;2;0;128;0m"
    GREEN1 = "\033[32m"
    GREEN2 = "\033[92m"
    GREEN3 = "\033[38;2;0;255;0m"

    YELLOW = "\033[33m"
    YELLOW1 = "\033[93m"
    YELLOW2 = "\033[38;2;255;255;0m"

    OLIVE = "\033[38;2;128;128;0m"

    BLUE = "\033[34m"
    BLUE1 = "\033[94m"
    BLUE2 = "\033[38;2;0;0;255m"
    BLUE3 = "\033[38;2;0;0;128m"

    MAGENTA = "\033[35m"
    MAGENTA1 = "\033[38;2;255;0;255m"

    PINK = "\033[95m"

    PURPLE = "\033[38;2;128;0;128m"

    CYAN = "\033[38;2;0;128;128m"
    CYAN1 = "\033[36m"
    CYAN2 = "\033[96m"

    ORANGE = "\033[38;5;208m"

    GRAY = "\033[90m"
    GRAY1 = "\033[37m"

    # Background Colors
    BG_BLACK = "\033[40m"
    BG_WHITE = "\033[107m"

    BG_GRAY = "\033[47m"
    BG_GRAY1 = "\033[100m"

    BG_RED = "\033[41m"
    BG_RED1 = "\033[101m"

    BG_GREEN = "\033[42m"
    BG_GREEN1 = "\033[102m"

    BG_YELLOW = "\033[103m"
    BG_OLIVE = "\033[43m"

    BG_BLUE = "\033[44m"
    BG_BLUE1 = "\033[104m"

    BG_MAGENTA = "\033[45m"

    BG_PINK = "\033[105m"

    BG_CYAN = "\033[46m"
    BG_CYAN1 = "\033[106m"

    BG_ORANGE = "\033[48;5;208m"
    BG_ORANGE1 = "\033[48;5;202m"
    BG_BROWN = "\033[48;5;166m"

    # Styles
    B = "\033[1m"
    IT = "\x1b[3m"
    U = "\x1b[4m"
    INV = "\u001b[7m"
    STR = "\u001b[9m"

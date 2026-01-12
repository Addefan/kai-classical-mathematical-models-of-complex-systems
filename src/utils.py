import sys

INVISIBLE_CHAR = "ㅤ"
BLACK_SQUARE = f"\033[40m{INVISIBLE_CHAR}\033[0m"
WHITE_SQUARE = f"\033[47m{INVISIBLE_CHAR}\033[0m"
GRAY_SQUARE = f"\033[100m{INVISIBLE_CHAR}\033[0m"


def clear_lines(n):
    sys.stdout.write(f"\x1b[{n}A\x1b[J")
    sys.stdout.flush()

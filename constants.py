from pygame import font

# RGB colours
RED = (100, 0, 50)
RED2 = (255, 0, 0)
BLACK = (0, 0, 0)
BLACK2 = (78, 75, 75)
WHITE = (255, 255, 255)
WHITE2 = (176, 190, 197)
GREEN = (31, 97, 52)
DARK_BLUE = (0, 143, 179)
ORANGE = (255, 204, 0)
PINK = (255, 0, 255)
YELLOW = (250, 253, 15)

# Game constants
""""
ROWS and COLS should be not even in order
to have normal fanorona board
"""
ROWS, COLS = 5, 9
FPS = 60
SOUND_EFFECTS = 1  # 1 - on, 0 - off
BOT_DELAY = 480

# Window constants
PADDING = 50
MIN_WIDTH = 250
MIN_HEIGHT = 250

# Drawing constants
font.init()
FONT = font.SysFont('calibri', 40, True)
FONT_SMALL = font.SysFont('calibri', 20, True)
LINE_WIDTH = 5
IF_DRAW_NUM_OF_ROUND = 1  # 1 - draw, 0 - dont't draw

# --------------------------------------
# check if ROWS and COLS are appropriate


def is_even(num):
    """Checks if a passed number is even"""
    if num % 2 == 0:
        return True
    return False


class BoardGeneratingError(Exception):
    def __init__(self):
        super().__init__(
            """Number of ROWS and COLS should be odd numbers,
you need to change constants""")


if is_even(ROWS) or is_even(COLS):
    """
    Check if ROWS and COLS are appropriate,
    otherwise raises BoardGeneratingError
    """
    raise BoardGeneratingError()


class MainArguemntRandomException(Exception):
    def __init__(self):
        super().__init__(
            """Random argument of main function should be
either 1 or 0, check documentation"""
        )


class MainArguemntCompException(Exception):
    def __init__(self):
        super().__init__(
            """Comp argument of main function should be
either 1 or 0, check documentation"""
        )


class WrongUseOfCaptureByAppOrWithFunc(Exception):
    def __init__(self):
        super().__init__(
            """Wrong use of function capture_by_approach()/
capture_by_withdrawal(), check documentation
for further information"""
        )

import pygame

# Required Colors's RGB Values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLUE1 = (52, 216, 235)
BLUE2 = (116, 133, 232)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# Textbox COlours
COLOR_INACTIVE = GRAY
COLOR_ACTIVE = BLACK

# Framerate
FPS = 60

# Total width and height of screen
WIDTH, HEIGHT = 800, 500

# Number of pixels
ROWS = 100


# Typings for strict-mode. Dont change
Surface = pygame.surface.Surface
rgb = tuple[int, int, int]
matrix_rgb = list[list[tuple[int, int, int]]]

# Background of Screen
BG_COLOR = WHITE

TITLE_FONT = "./pixel.ttf"


def get_titlefont(size: int):
    return pygame.font.Font(TITLE_FONT, size)


FONT = "./mono.ttf"


def get_font(size: int):
    return pygame.font.Font(FONT, size)

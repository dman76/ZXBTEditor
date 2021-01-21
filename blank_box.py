
import pygame as pg
import sys

screen = pg.display.set_mode((1200, 960))
BLACK = (0, 0, 0)

def blank_box(selected):
    boxes = {
        0: (1013, 3, 132, 132),    # Blank Selected Building picture box
        1: (981, 151, 198, 28),    # Blank Selected Text Box
        2: (981, 251, 198, 28),    # Blank Secondary text  box
        3: (981, 301, 198, 648),   # Blank long text information box
        4: (1057, 197, 48, 40)     # Blank coordinates box
    }

    coords = boxes.get(selected, None)

    if coords:
        pg.draw.rect(screen, BLACK, coords)

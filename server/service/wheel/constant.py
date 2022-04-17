from dataclasses import dataclass

import numpy as np


@dataclass
class Point:
    x: int
    y: int


# WHEEL

WHEEL_RADIUS = 150
WHEEL_WIDTH = 300
WHEEL_HEIGHT = 300
WHEEL_CENTER = Point(x=WHEEL_WIDTH / 2, y=WHEEL_HEIGHT / 2)
TRIANGLE_SIZE = 20

# GIF

NB_FRAMES = 100
LEGEND_WIDTH = 200
LEGEND_FONT_SIZE = 20
LEGEND_SPACING = 4
LEGEND_LEFT_STARTING_SPACING = LEGEND_SPACING * 6
LEGEND_TOP_STARTING_SPACING = LEGEND_SPACING * 5

# COLORS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = np.array(
    [
        np.array([52, 152, 219], dtype=np.uint8),
        np.array([231, 76, 60], dtype=np.uint8),
        np.array([46, 204, 113], dtype=np.uint8),
        np.array([230, 126, 34], dtype=np.uint8),
        np.array([26, 188, 156], dtype=np.uint8),
        np.array([241, 196, 15], dtype=np.uint8),
        np.array([155, 89, 182], dtype=np.uint8),
        np.array([52, 73, 94], dtype=np.uint8),
        np.array([149, 165, 166], dtype=np.uint8),
        np.array([41, 128, 185], dtype=np.uint8),
        np.array([192, 57, 43], dtype=np.uint8),
        np.array([39, 174, 96], dtype=np.uint8),
        np.array([211, 84, 0], dtype=np.uint8),
        np.array([22, 160, 133], dtype=np.uint8),
        np.array([243, 156, 18], dtype=np.uint8),
        np.array([142, 68, 173], dtype=np.uint8),
        np.array([44, 62, 80], dtype=np.uint8),
        np.array([127, 140, 141], dtype=np.uint8),
        np.array([52, 152, 219], dtype=np.uint8),
        np.array([231, 76, 60], dtype=np.uint8),
        np.array([46, 204, 113], dtype=np.uint8),
        np.array([230, 126, 34], dtype=np.uint8),
        np.array([26, 188, 156], dtype=np.uint8),
        np.array([241, 196, 15], dtype=np.uint8),
        np.array([155, 89, 182], dtype=np.uint8),
        np.array([52, 73, 94], dtype=np.uint8),
        np.array([149, 165, 166], dtype=np.uint8),
        np.array([41, 128, 185], dtype=np.uint8),
        np.array([192, 57, 43], dtype=np.uint8),
        np.array([39, 174, 96], dtype=np.uint8),
        np.array([211, 84, 0], dtype=np.uint8),
        np.array([22, 160, 133], dtype=np.uint8),
        np.array([243, 156, 18], dtype=np.uint8),
        np.array([142, 68, 173], dtype=np.uint8),
        np.array([44, 62, 80], dtype=np.uint8),
        np.array([127, 140, 141], dtype=np.uint8),
    ]
)

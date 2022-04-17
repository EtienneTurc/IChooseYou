import numpy as np
import pytest
from PIL import ImageFont

from server.service.wheel.constant import COLORS, LEGEND_WIDTH, WHEEL_HEIGHT
from server.service.wheel.image_helper import build_legend, elipsis_text


@pytest.mark.parametrize(
    "text, font_size, available_space, expected_text",
    [
        ("Lorem", 20, 200, "Lorem"),
        ("Lorem ipsum dolor sit amet", 20, 200, "Lorem ipsum dolor s..."),
        ("Lorem ipsum dolor sit", 20, 200, "Lorem ipsum dolor sit"),
        ("Lorem ipsum dolor sit amet", 10, 200, "Lorem ipsum dolor sit amet"),
        ("Lorem ipsum dolor sit amet", 20, 100, "Lorem ip..."),
    ],
)
def test_elipsis_text(text, font_size, available_space, expected_text):
    font = ImageFont.truetype("assets/font/arial.ttf", font_size)
    assert elipsis_text(text, font, available_space) == expected_text


@pytest.mark.parametrize(
    "number_of_names, expected_legend_size",
    [
        (1, (WHEEL_HEIGHT, LEGEND_WIDTH, 3)),
        (9, (WHEEL_HEIGHT, LEGEND_WIDTH, 3)),
        (10, (WHEEL_HEIGHT, LEGEND_WIDTH * 2, 3)),
        (20, (WHEEL_HEIGHT, LEGEND_WIDTH * 3, 3)),
        (27, (WHEEL_HEIGHT, LEGEND_WIDTH * 3, 3)),
        (30, (WHEEL_HEIGHT, LEGEND_WIDTH * 3, 3)),
    ],
)
def test_build_legend(number_of_names, expected_legend_size):
    names = ["1"] * number_of_names
    assert np.shape(build_legend(names, COLORS)) == expected_legend_size

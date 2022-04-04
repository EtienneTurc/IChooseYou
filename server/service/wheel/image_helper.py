import numpy as np
from PIL import Image, ImageDraw, ImageFont

from server.service.wheel.constant import (BLACK, LEGEND_FONT_SIZE, LEGEND_WIDTH,
                                           WHEEL_HEIGHT, WHITE)


def save_gif(file_name, frames):
    images = [Image.fromarray(frame, mode="RGB") for frame in frames]
    images[0].encoderinfo = {"loop": 0}  # Hack to set 0 loop
    images[0].save(
        file_name,
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=50,
        quality=3,
        format="GIF",
    )


def build_legend(names, colors):
    spacing = 4
    square_size = LEGEND_FONT_SIZE
    x_offset = spacing * 6
    y_offset = spacing * 5

    legend_canvas = Image.new("RGB", (LEGEND_WIDTH, WHEEL_HEIGHT), WHITE)
    drawing_context = ImageDraw.Draw(legend_canvas)
    font = ImageFont.truetype("assets/font/arial.ttf", LEGEND_FONT_SIZE)

    for i, name in enumerate(names):
        color = colors[i]

        start_x = x_offset
        start_y = y_offset + (LEGEND_FONT_SIZE + spacing * 2) * i

        drawing_context.rectangle(
            (
                (start_x, start_y),
                (start_x + square_size, start_y + square_size),
            ),
            fill=(color[0], color[1], color[2]),
        )

        drawing_context.text(
            (start_x + 2 * spacing + square_size, start_y),
            name,
            font=font,
            fill=BLACK,
        )
    return np.asarray(legend_canvas)

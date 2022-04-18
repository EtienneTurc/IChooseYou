import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from server.service.wheel.constant import (BLACK, LEGEND_FONT_SIZE,
                                           LEGEND_LEFT_STARTING_SPACING, LEGEND_SPACING,
                                           LEGEND_TOP_STARTING_SPACING, LEGEND_WIDTH,
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


def text_dichotomy(text, font, available_space_for_text):
    half_text = text[: len(text) // 2]
    upper_half_text = text[: (1 + len(text) // 2)]

    half_text_size = font.getsize(half_text)[0]
    upper_half_text_size = font.getsize(upper_half_text)[0]

    if (
        half_text_size <= available_space_for_text
        and upper_half_text_size > available_space_for_text
    ):
        return half_text

    if half_text_size > available_space_for_text:
        return text_dichotomy(half_text, font, available_space_for_text)

    return half_text + text_dichotomy(
        text[(len(text) // 2):], font, available_space_for_text - half_text_size
    )


def elipsis_text(text, font, available_space):
    text_size = font.getsize(text)[0]

    if available_space > text_size:
        return text

    dots_size = font.getsize("...")[0]
    available_space_for_text = available_space - dots_size
    return text_dichotomy(text, font, available_space_for_text) + "..."


def build_legend_in_batch(names, colors):
    square_size = LEGEND_FONT_SIZE
    x_offset = LEGEND_LEFT_STARTING_SPACING
    y_offset = LEGEND_TOP_STARTING_SPACING
    available_name_space = LEGEND_WIDTH - x_offset - (2 * LEGEND_SPACING + square_size)

    legend_canvas = Image.new("RGB", (LEGEND_WIDTH, WHEEL_HEIGHT), WHITE)
    drawing_context = ImageDraw.Draw(legend_canvas)
    font = ImageFont.truetype("assets/font/arial.ttf", LEGEND_FONT_SIZE)

    for i, name in enumerate(names):
        color = colors[i]

        start_x = x_offset
        start_y = y_offset + (LEGEND_FONT_SIZE + LEGEND_SPACING * 2) * i

        drawing_context.rectangle(
            (
                (start_x, start_y),
                (start_x + square_size, start_y + square_size),
            ),
            fill=(color[0], color[1], color[2]),
        )

        drawing_context.text(
            (start_x + 2 * LEGEND_SPACING + square_size, start_y),
            elipsis_text(name, font, available_name_space),
            font=font,
            fill=BLACK,
        )
    return np.asarray(legend_canvas)


def build_legend(names, colors):
    batch_size = int(
        (WHEEL_HEIGHT - LEGEND_TOP_STARTING_SPACING * 2)
        / (LEGEND_FONT_SIZE + LEGEND_SPACING * 2)
    )
    number_of_batch = min(3, math.ceil(len(names) / batch_size))

    legend = None
    for batch_index in range(number_of_batch):
        names_in_batch = names[batch_index::number_of_batch][:batch_size]
        colors_in_batch = colors[batch_index::number_of_batch][:batch_size]
        legend_in_batch = build_legend_in_batch(names_in_batch, colors_in_batch)
        legend = (
            np.concatenate((legend, legend_in_batch), axis=1)
            if legend is not None
            else legend_in_batch
        )

    return legend

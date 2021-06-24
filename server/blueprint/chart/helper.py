import numpy as np


def get_colors(size, offset=0):
    return np.linspace(0 + offset, 255 + offset, size + 1)[:size]


def map_item_to_color(pick_list):
    colors = get_colors(len(pick_list))

    item_to_color = {}
    for i in range(len(pick_list)):
        item_to_color[pick_list[i]] = int(colors[i])

    return item_to_color

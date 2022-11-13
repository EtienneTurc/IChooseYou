import io
import math

from PIL import Image

from server.blueprint.chart.helper import map_item_to_color
from server.orm.command import Command
from server.service.strategy.helper import get_strategy

saturation = 220
lightness = 200


def create_heat_map(command_name: str, channel_id: str) -> tuple[any, str]:
    command = Command.find_one_by_name_and_chanel(command_name, channel_id)
    item_to_color = map_item_to_color(command.pick_list)
    strategy = get_strategy(
        command.strategy, pick_list=command.pick_list, weight_list=command.weight_list
    )

    n = len(command.pick_list)
    initial_img_size = int(max(100 / n, math.ceil(100 / n)) * n)
    img_final_size = 5 * initial_img_size

    img = Image.new("HSV", (initial_img_size, initial_img_size), "black")
    pixels = img.load()

    selected_items = strategy.select(
        number_of_items_to_select=img.size[0] * img.size[1]
    )

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            selected_item = selected_items[i * img.size[1] + j]
            pixels[i, j] = (
                item_to_color[selected_item],
                saturation,
                lightness,
            )

    img = img.resize((img_final_size, img_final_size), Image.NEAREST)
    img = img.convert(mode="RGB")

    file_buffer = io.BytesIO()
    img.save(file_buffer, "png")
    file_buffer.seek(0)

    mimetype = "image/png"

    return file_buffer, mimetype

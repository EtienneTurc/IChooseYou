import random

import numpy as np

from server.service.slack.helper import get_user_id_in_mention, is_mention
from server.service.slack.sdk_wrapper import is_user_of_team_active


def select_from_pick_list(
    pick_list: list[str],
    weight_list: list[float],
    team_id: str = None,
    only_active_users: bool = False,
) -> str:
    if not pick_list or not len(pick_list) or not weight_list or not len(weight_list):
        return None

    [selected_element] = random.choices(pick_list, weights=weight_list)

    if not only_active_users:
        return selected_element

    if not is_mention(selected_element):
        return selected_element

    user_mentionned = get_user_id_in_mention(selected_element)
    if is_user_of_team_active(team_id, user_mentionned):
        return selected_element

    selected_element_index = pick_list.index(selected_element)
    selected_element_weight = weight_list[selected_element_index]
    new_pick_list = [el for el in pick_list if el != selected_element]
    new_weight_list = (
        weight_list[:selected_element_index]
        + weight_list[(selected_element_index + 1):]
    )

    if selected_element_weight == np.sum(weight_list) and len(new_weight_list):
        new_weight_list[selected_element_index % len(new_weight_list)] = 1

    return select_from_pick_list(
        new_pick_list, new_weight_list, team_id, only_active_users=only_active_users
    )

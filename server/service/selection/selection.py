import random

import numpy as np

from server.service.helper.dict_helper import normalize
from server.service.slack.helper import get_user_id_in_mention, is_mention
from server.service.slack.sdk_helper import is_user_of_team_active
from server.service.strategy.helper import get_strategy


def select_from_pick_list(
    pick_list: list[str],
    weight_list: list[float],
    strategy_name: str,
    number_of_items_to_select: int = 1,
    team_id: str = None,
    only_active_users: bool = False,
) -> list[str]:
    selected_items = []
    for _ in range(number_of_items_to_select):
        selected_item, new_pick_list, new_weight_list = select_one_from_pick_list(
            pick_list, weight_list, team_id, only_active_users
        )
        selected_items.append(selected_item)

        if len(new_weight_list):
            strategy = get_strategy(strategy_name, new_weight_list)
            strategy.update(indices_selected=[new_pick_list.index(selected_item)])
            new_weight_list = strategy.weight_list

            new_pick_list, new_weight_list = remove_item(
                selected_item, new_pick_list, new_weight_list
            )
        pick_list, weight_list = new_pick_list, new_weight_list

    return selected_items


def select_one_from_pick_list(
    pick_list: list[str],
    weight_list: list[float],
    team_id: str = None,
    only_active_users: bool = False,
) -> tuple[str, list[str], list[float]]:
    if not pick_list or not len(pick_list) or not weight_list or not len(weight_list):
        return None, [], []

    [selected_item] = random.choices(pick_list, weights=weight_list)

    if not only_active_users or not is_mention(selected_item):
        return selected_item, pick_list, weight_list

    user_mentionned = get_user_id_in_mention(selected_item)
    if is_user_of_team_active(team_id=team_id, user_id=user_mentionned):
        return selected_item, pick_list, weight_list

    new_pick_list, new_weight_list = remove_item(selected_item, pick_list, weight_list)

    return select_one_from_pick_list(
        new_pick_list, new_weight_list, team_id, only_active_users=only_active_users
    )


def remove_item(
    item_to_remove: str, pick_list: list[str], weight_list: list[float]
) -> tuple[list[str], list[float]]:
    # Update pick list and weight list
    item_to_remove_index = pick_list.index(item_to_remove)
    item_to_remove_weight = weight_list[item_to_remove_index]
    new_pick_list = [el for el in pick_list if el != item_to_remove]
    new_weight_list = (
        weight_list[:item_to_remove_index] + weight_list[(item_to_remove_index + 1):]
    )

    # Round robin support
    if item_to_remove_weight == np.sum(weight_list) and len(new_weight_list):
        new_weight_list[item_to_remove_index % len(new_weight_list)] = 1

    if new_weight_list:
        new_weight_list = normalize(new_weight_list)

    return new_pick_list, new_weight_list

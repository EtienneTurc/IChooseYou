import random

import numpy as np

from server.service.helper.dict_helper import normalize
from server.service.selection.assertion import assert_pick_list
from server.service.slack.helper import get_user_id_in_mention, is_mention
from server.service.slack.sdk_helper import is_user_of_team_active
from server.service.strategy.helper import get_strategy


def clean_and_select_from_pick_list(
    *,
    pick_list: list[str],
    weight_list: list[float],
    user_id: str,
    strategy_name: str,
    number_of_items_to_select: int,
    team_id: str,
    only_active_users: bool,
    self_exclude: bool,
) -> list[str]:
    initial_pick = pick_list[:]
    pick_list, weight_list = exclude_user_from_pick_list(
        pick_list=pick_list,
        weight_list=weight_list,
        user_id=user_id,
        self_exclude=self_exclude,
    )

    assert_pick_list(pick_list, len(pick_list) != len(initial_pick))
    if only_active_users:
        pick_list, weight_list = remove_inactive_users_from_pick_list(
            team_id=team_id, pick_list=pick_list, weight_list=weight_list
        )

    return (
        select_from_pick_list(
            initial_pick_list=pick_list[:],
            initial_weight_list=weight_list[:],
            strategy_name=strategy_name,
            number_of_items_to_select=number_of_items_to_select,
        ),
        pick_list,
        weight_list,
    )


def select_from_pick_list(
    *,
    initial_pick_list: list[str],
    initial_weight_list: list[float],
    strategy_name: str,
    number_of_items_to_select: int,
) -> list[str]:
    selected_items = []
    pick_list = initial_pick_list[:]
    weight_list = initial_weight_list[:]

    for _ in range(number_of_items_to_select):
        selected_item, new_pick_list, new_weight_list = select_one_from_pick_list(
            pick_list, weight_list
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
        if not len(pick_list) or not len(weight_list):
            pick_list, weight_list = initial_pick_list, initial_weight_list

    return selected_items


def select_one_from_pick_list(
    pick_list: list[str],
    weight_list: list[float],
) -> tuple[str, list[str], list[float]]:
    if not pick_list or not len(pick_list) or not weight_list or not len(weight_list):
        return None, [], []
    [selected_item] = random.choices(pick_list, weights=weight_list)
    return selected_item, pick_list, weight_list


def remove_item(
    item_to_remove: str, pick_list: list[str], weight_list: list[float]
) -> tuple[list[str], list[float]]:
    # Update pick list and weight list
    item_to_remove_index = pick_list.index(item_to_remove)
    item_to_remove_weight = weight_list[item_to_remove_index]
    new_pick_list = (
        pick_list[:item_to_remove_index] + pick_list[(item_to_remove_index + 1):]
    )
    new_weight_list = (
        weight_list[:item_to_remove_index] + weight_list[(item_to_remove_index + 1):]
    )

    # Round robin support
    if item_to_remove_weight == np.sum(weight_list) and len(new_weight_list):
        new_weight_list[item_to_remove_index % len(new_weight_list)] = 1

    if new_weight_list:
        new_weight_list = normalize(new_weight_list)

    return new_pick_list, new_weight_list


def exclude_user_from_pick_list(
    *, pick_list: list[str], weight_list: dict[float], user_id: str, self_exclude: bool
):
    if not self_exclude or not user_id:
        return pick_list, weight_list

    indices_of_items_to_remove = [
        index for index, item in enumerate(pick_list) if user_id in item
    ]
    pick_list = [
        item
        for index, item in enumerate(pick_list)
        if index not in indices_of_items_to_remove
    ]
    weight_list = normalize(
        [
            item
            for index, item in enumerate(weight_list)
            if index not in indices_of_items_to_remove
        ]
    )
    return pick_list, weight_list


def remove_inactive_users_from_pick_list(
    *, team_id: str, pick_list: list[str], weight_list: list[str]
):
    new_pick_list = pick_list[:]
    new_weight_list = weight_list[:]

    for item in pick_list:
        user_mentionned = get_user_id_in_mention(item)
        if is_mention(item) and not is_user_of_team_active(
            team_id=team_id, user_id=user_mentionned
        ):
            new_pick_list, new_weight_list = remove_item(
                item, new_pick_list, new_weight_list
            )

    return new_pick_list, new_weight_list

from server.service.error.type.bad_request_error import BadRequestError
from server.service.strategy.base import BaseStrategy


def get_values_to_update(
    pick_list: list[str],
    new_pick_list: list[str] = None,
    items_to_add: list[str] = None,
    items_to_remove: list[str] = None,
) -> tuple[list[str], list]:
    pick_list_set = set(pick_list)

    if new_pick_list:
        items_to_add = list(set(new_pick_list) - pick_list_set)
        items_to_remove = list(pick_list_set - set(new_pick_list))

    values_to_add_to_pick_list = (
        list(set(items_to_add) - pick_list_set) if items_to_add else []
    )

    values_to_remove_from_pick_list = (
        list(pick_list_set.intersection(set(items_to_remove)))
        if items_to_remove
        else []
    )

    return values_to_add_to_pick_list, values_to_remove_from_pick_list


def get_indices_of_items_to_remove(
    pick_list: list[str],
    values_to_remove_from_pick_list: list[str],
) -> list[int]:
    return [
        index
        for index, el in enumerate(pick_list)
        if el in values_to_remove_from_pick_list
    ]


def compute_new_weight_list(
    strategy: BaseStrategy,
    values_to_add_to_pick_list: list[str],
    indices_of_items_to_remove: list[int],
) -> list[float]:
    strategy.add_items(len(values_to_add_to_pick_list))
    strategy.remove_items(indices_of_items_to_remove)
    return strategy.weight_list


def compute_new_pick_list(
    pick_list: list[str],
    values_to_add_to_pick_list: list[str],
    indices_of_items_to_remove: list[int],
) -> list[str]:
    new_pick_list = [*pick_list, *values_to_add_to_pick_list]
    return [
        item
        for index, item in enumerate(new_pick_list)
        if index not in indices_of_items_to_remove
    ]


def assert_pick_list_can_be_updated(
    number_of_items_in_pick_list: int,
    number_of_items_to_add: int,
    number_of_items_to_remove: int,
) -> None:
    if (
        not number_of_items_to_add
        and number_of_items_in_pick_list == number_of_items_to_remove
    ):
        raise BadRequestError("Can't remove all the items in the pick list.")

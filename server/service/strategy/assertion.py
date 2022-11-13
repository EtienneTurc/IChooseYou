import numpy as np

from server.service.error.type.consistency_error import ConsistencyError
from server.service.error.type.missing_element_error import MissingElementError


def assert_pick_list_is_not_empty(pick_list) -> None:
    if not len(pick_list):
        raise ConsistencyError("Can't pick an item from an empty pick list.")


def assert_weight_list_is_not_empty(weight_list) -> None:
    if not len(weight_list):
        raise ConsistencyError("Weight list must not be empty.")


def assert_pick_list_has_same_size_than_weight_list(pick_list, weight_list) -> None:
    if len(pick_list) != len(weight_list):
        raise ConsistencyError("Pick list and weight list muse have the same length.")


def assert_weight_list_must_sum_up_to_1(weight_list) -> None:
    if round(np.sum(weight_list), 6) != 1:
        raise ConsistencyError("Weight list must sum up to 1.")


def assert_pick_list_valid_after_self_exclusion(pick_list: list[str]) -> None:
    if not len(pick_list):
        message = "Pick list contains only the user using the command."
        message += (
            " And the option to exclude the current user from the pick is enabled."
        )
        message += " Thus no item can be picked from the pick list."
        raise MissingElementError(message)


def assert_pick_list_valid_after_filtering_inactive_users(pick_list: list[str]) -> None:
    if not len(pick_list):
        message = "All users in the pick list are inactive."
        message += " And the option to exclude inactive users is enabled."
        message += " Thus no item can be picked from the pick list."
        raise MissingElementError(message)

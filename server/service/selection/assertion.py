from server.service.error.type.bad_request_error import BadRequestError
from server.service.error.type.consistency_error import ConsistencyError


def assert_pick_list(pick_list: list[str], item_excluded: bool) -> None:
    if not len(pick_list) and item_excluded:
        message = "Pick list contains only the user using the command."
        message += " But the flag selfExclude is set to True."
        message += " Thus no item can be picked from the pick list."
        raise BadRequestError(message)

    if not len(pick_list):
        raise ConsistencyError("Can't pick an item from an empty pick list.")

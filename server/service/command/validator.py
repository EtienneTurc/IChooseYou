from flask import current_app

from server.service.command.args import ArgError
from server.service.error.back_error import BackError
from server.service.strategy.enum import Strategy


def assert_pick_list_can_be_updated(
    number_of_elements_in_pick_list: int,
    number_of_elements_to_add: int,
    number_of_elements_to_remove: int,
) -> None:
    if (
        not number_of_elements_to_add
        and number_of_elements_in_pick_list == number_of_elements_to_remove
    ):
        raise BackError("Can't remove all the elements in the pick list.", 400)


def assert_strategy_is_valid(strategy_name: str) -> None:
    if strategy_name and strategy_name not in Strategy._member_names_:
        error_message = f"{strategy_name} is not a valid strategy."
        error_message += (
            f"\nValid strategies are: {', '.join(Strategy._member_names_)}."
        )
        raise BackError(error_message, 400)


def assert_pick_list(pick_list: list[str], element_excluded: bool) -> None:
    if not len(pick_list) and element_excluded:
        message = "Pick list contains only the user using the command."
        message += "But the flag selfExclude is set to True."
        message += "Thus no element can be picked from the pick list."
        raise ArgError(None, message)

    if not len(pick_list):
        raise BackError("Can't pick an element from an empty pick list.", 400)


def assert_selected_element(
    selected_element: str, only_active_users: bool, command_name: str
) -> None:
    if selected_element is None:
        if only_active_users:
            message = "No active users to select found."
            message += " If you want to select non active users"
            message += (
                " consider updating the command with the following slash command:\n"
            )
            message += f"`{current_app.config['SLASH_COMMAND']} update {command_name} -o false`"  # noqa E501
            raise BackError(message, 404)

        raise BackError("Could not find an element to select", 500)

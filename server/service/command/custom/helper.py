from flask import current_app

from server.service.error.type.consistency_error import ConsistencyError
from server.service.error.type.missing_element_error import MissingElementError


def create_custom_command_label(command_label: str, additional_text: str) -> str:
    space = " " if command_label and additional_text else ""
    return f"{command_label}{space}{additional_text}"


def assert_selected_items(
    selected_items: list[str], only_active_users: bool, command_name: str
) -> None:
    for selected_item in selected_items:
        if selected_item is None:
            if only_active_users:
                message = "No active users to select found."
                message += " If you want to select non active users"
                message += (
                    " consider updating the command with the following slash command:\n"
                )
                message += f"`{current_app.config['SLASH_COMMAND']} update {command_name} -o false`"  # noqa E501
                raise MissingElementError(message)

            raise ConsistencyError("Could not find an item to select")

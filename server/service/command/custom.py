from dataclasses import dataclass

from flask import current_app

from server.service.command.args import ArgError
from server.service.command.utils import select_from_pick_list
from server.service.error.back_error import BackError
from server.service.slack.message import Message, MessageVisibility
from server.service.slack.message_formatting import format_custom_command_message


@dataclass
class CustomCommand:
    name: str
    label: str
    pick_list: list
    self_exclude: bool
    only_active_users: bool

    def exec(
        self, user_id: str, text: str, team_id: str = None, **kwargs
    ) -> tuple[Message, str]:
        pick_list = self.pick_list
        if self.self_exclude and user_id:
            pick_list = [el for el in pick_list if user_id not in el]

        self._assert_pick_list(pick_list, user_id)

        selected_element = select_from_pick_list(
            pick_list, team_id, only_active_users=self.only_active_users
        )
        self._assert_selected_element(selected_element)

        label = self._create_label(text)
        return (
            Message(
                content=format_custom_command_message(user_id, selected_element, label),
                visibility=MessageVisibility.NORMAL,
                as_attachment=False,
            ),
            selected_element,
        )

    def _create_label(self, text: str) -> str:
        space = " " if self.label and text else ""
        return f"{self.label}{space}{text}"

    def _assert_pick_list(self, pick_list: list[str], user_id: str) -> None:
        if not len(pick_list):
            if not len(self.pick_list):
                raise ArgError(None, "Can't pick an element from an empty pick list.")

            if len(self.pick_list) == 1 and user_id and user_id in self.pick_list[0]:
                message = "Pick list contains only the user using the command."
                message += "But the flag selfExclude is set to True."
                message += "Thus no element can be picked from the pick list."
                raise ArgError(None, message)

            raise BackError("Pick list empty.", 500)

    def _assert_selected_element(self, selected_element: str) -> None:
        if selected_element is None:
            if self.only_active_users:
                message = "No active users to select found."
                message += " If you want to select non active users"
                message += (
                    " consider updating the command with the following slash command:\n"
                )
                message += f"`{current_app.config['SLASH_COMMAND']} update {self.name} -o false`"  # noqa E501
                raise BackError(message, 404)

            raise BackError("Could not find an element to select", 500)

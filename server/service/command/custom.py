from dataclasses import dataclass

from server.service.command.validator import assert_pick_list, assert_selected_element
from server.service.selection.selection import select_from_pick_list
from server.service.slack.message import Message, MessageVisibility
from server.service.slack.message_formatting import format_custom_command_message


@dataclass
class CustomCommand:
    name: str
    label: str
    pick_list: list[str]
    weight_list: list[float]
    strategy: str
    self_exclude: bool
    only_active_users: bool

    def exec(
        self, user_id: str, text: str, team_id: str = None, **kwargs
    ) -> tuple[Message, str]:
        pick_list = self.pick_list
        weight_list = self.weight_list
        if self.self_exclude and user_id:
            indices_of_elements_to_remove = [
                index for index, element in enumerate(pick_list) if user_id in element
            ]
            pick_list = [
                element
                for index, element in enumerate(pick_list)
                if index not in indices_of_elements_to_remove
            ]
            weight_list = [
                element
                for index, element in enumerate(weight_list)
                if index not in indices_of_elements_to_remove
            ]

        assert_pick_list(pick_list, len(pick_list) != len(self.pick_list))

        selected_element = select_from_pick_list(
            pick_list, weight_list, team_id, only_active_users=self.only_active_users
        )
        assert_selected_element(selected_element, self.only_active_users, self.name)

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

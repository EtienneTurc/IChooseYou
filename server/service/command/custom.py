import random
from dataclasses import dataclass

from server.service.command.args import ArgError
from server.service.error.back_error import BackError
from server.service.slack.message_formatting import format_custom_command_message
from server.service.slack.message import Message, MessageVisibility


@dataclass
class CustomCommand:
    name: str
    label: str
    pick_list: list
    self_exclude: bool

    def exec(self, user_id: int, text: str, **kwargs):
        pick_list = self.pick_list
        if self.self_exclude:
            pick_list = [el for el in pick_list if str(user_id) not in el]

        if not len(pick_list):
            if not len(self.pick_list):
                raise ArgError(None, "Can't pick an element from an empty pick list.")

            if len(self.pick_list) == 1 and str(user_id) in self.pick_list[0]:
                message = "Pick list contains only the user using the command."
                message += "But the flag selfExclude is set to True."
                message += "Thus no element can be picked from the pick list."
                raise ArgError(None, message)

            else:
                raise BackError("Pick list empty.", 500)

        selected_element = random.choice(pick_list)
        label = self._create_label(text)
        return Message(
            content=format_custom_command_message(user_id, selected_element, label),
            visibility=MessageVisibility.NORMAL,
            as_attachment=False,
        )

    def _create_label(self, text: str) -> str:
        space = " " if self.label and text else ""
        return f"{self.label}{space}{text}"

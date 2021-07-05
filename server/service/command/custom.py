from dataclasses import dataclass

from server.service.command.args import Arg, ArgumentParser
from server.service.command.option_cleaning import format_text_to_list, options_to_dict
from server.service.command.validator import assert_pick_list, assert_selected_items
from server.service.helper.dict_helper import normalize
from server.service.selection.selection import select_from_pick_list
from server.service.slack.message import Message, MessageVisibility
from server.service.slack.message_formatting import format_custom_command_message


@dataclass
class CustomCommand:
    name: str
    label: str
    text: str
    pick_list: list[str]
    weight_list: list[float]
    strategy: str
    self_exclude: bool
    only_active_users: bool
    number_of_items_to_select: int = 1

    def __post_init__(self):
        args = [
            Arg(
                name="number-of-items-to-select",
                short="n",
                nargs="?",
                type=int,
                required=False,
            )
        ]
        options = self._get_options_and_clean_text(args)
        self.number_of_items_to_select = (
            options.get("number_of_items_to_select")
            if options.get("number_of_items_to_select")
            else 1
        )

    def exec(self, user_id: str, team_id: str = None, **kwargs) -> tuple[Message, str]:
        pick_list = self.pick_list
        weight_list = self.weight_list
        if self.self_exclude and user_id:
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

        assert_pick_list(pick_list, len(pick_list) != len(self.pick_list))

        selected_items = select_from_pick_list(
            pick_list,
            weight_list,
            self.strategy,
            number_of_items_to_select=self.number_of_items_to_select,
            team_id=team_id,
            only_active_users=self.only_active_users,
        )
        assert_selected_items(selected_items, self.only_active_users, self.name)

        label = self._create_label()
        return (
            Message(
                content=format_custom_command_message(user_id, selected_items, label),
                visibility=MessageVisibility.NORMAL,
                as_attachment=False,
            ),
            selected_items,
        )

    def _create_label(self) -> str:
        space = " " if self.label and self.text else ""
        return f"{self.label}{space}{self.text}"

    def _get_options_and_clean_text(self, args: list[Arg]) -> dict[str, any]:
        # Parse text
        parser = ArgumentParser(prog=self.name, exit_on_error=False, add_help=False)
        text_list = format_text_to_list(self.text)
        for arg in args:
            arg.add_to_parser(parser)
        options, _ = parser.parse_known_args(text_list)
        options = options_to_dict(options.__dict__, args)

        # Clean text
        for arg in args:
            if options.get(arg.variable_name):
                self.text = self.text.replace(
                    f"{arg.prefix}{arg.name} {options.get(arg.variable_name)}", ""
                )
                self.text = self.text.replace(
                    f"-{arg.short} {options.get(arg.variable_name)}", ""
                )

                self.text = self.text.strip()

        return options

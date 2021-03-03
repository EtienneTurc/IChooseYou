import random
from dataclasses import dataclass

from server.command.args import ArgumentParser
from server.command.utils import (
    find_args_in_text,
    format_text_to_list,
    get_args_in_label,
    options_to_dict,
)
from server.command.validator import assert_named_args, assert_positional_args


@dataclass
class CustomCommand:
    name: str
    label: str
    pick_list: list
    self_exclude: bool

    def exec(self, user, args_text):
        pick_list = self.pick_list
        if self.self_exclude:
            pick_list = [el for el in pick_list if user["id"] not in el]

        selected_element = random.choice(pick_list)
        label = self._create_label(args_text)
        message = (
            f"Hey ! <@{user['id']}|{user['name']}> choose {selected_element} to {label}"
        )

        return message

    def _create_label(self, args_text):
        req_positional_args, req_named_args = find_args_in_text(args_text)
        positional_args, named_args = get_args_in_label(self.label)

        assert_positional_args(req_positional_args, positional_args)
        assert_named_args(req_named_args, named_args)

        label = self.label
        # Replace positional args
        for index, arg in enumerate(req_positional_args):
            label = label.replace(f"${index + 1}", arg.name)

        # Replace named args
        n = len(req_positional_args)
        parser = ArgumentParser(prog=self.name, exit_on_error=False)
        for arg in req_named_args:
            arg.add_to_parser(parser)

        args_list = format_text_to_list(args_text)[n:]
        options = parser.parse_args(args_list)
        options = options_to_dict(options.__dict__, req_named_args)

        for option_name in options:
            label = label.replace(f"${option_name}", options[option_name])

        return label

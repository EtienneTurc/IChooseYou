from dataclasses import dataclass
import random
from .args import find_args_in_text
from .utils import get_args_in_label, get_as_string
import argparse


@dataclass
class CustomCommand:
    name: str
    label: str
    pick_list: list
    self_exclude: bool

    def exec(self, user, args_text):
        pick_list = self.pick_list
        if self.self_exclude:
            pick_list = [el for el in pick_list if user.id not in el]

        selected_element = random.choice(pick_list)
        label = self._create_label(args_text)
        message = f"Hey ! @{user['name']} choose {selected_element} to {label}"

        print(message)

        return message

    def _create_label(self, args_text):
        req_positional_args, req_named_args = find_args_in_text(args_text)
        positional_args, named_args = get_args_in_label(self.label)

        # TODO assert args_text is correts
        # if first_arg_index !=

        label = self.label
        # Replace positional args
        for index, arg in enumerate(req_positional_args):
            label = label.replace(f"${index + 1}", arg.name)

        # Replace named args
        n = len(req_positional_args)
        if not n:
            return label

        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)

        for arg in req_named_args:
            arg.add_to_parser(parser)

        # TODO try catch options
        options = parser.parse_args(args_text.split(" ")[n:]).__dict__

        for option_name in options:
            label = label.replace(
                f"${option_name}", get_as_string(options, option_name)
            )

        return label

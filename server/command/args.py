from dataclasses import dataclass


@dataclass
class Arg:
    name: str
    nargs: int = 1
    default: any = None

    def add_to_parser(self, parser, prefix="--"):
        arg = dict(self.__dict__)
        del arg["name"]
        parser.add_argument(f"{prefix}{self.name}", **arg)
        return parser


class ArgError(Exception):
    def __init__(self, message):
        self.message = message


def find_args_in_text(text):
    text_list = text.split(" ")
    first_arg_index = -1

    named_args = []
    for index, word in enumerate(text_list):
        if word[:2] == "--":
            if first_arg_index == -1:
                first_arg_index = index
            named_args.append(Arg(name=word[2:], nargs="*"))

    positional_args = []
    if first_arg_index != -1:
        for word in text_list[:first_arg_index]:
            positional_args.append(Arg(name=word))

    return positional_args, named_args

import argparse
from dataclasses import dataclass
from typing import NoReturn

ArgError = argparse.ArgumentError


class ArgumentParser(argparse.ArgumentParser):
    def exit(self, status: int = 0, message: str = None) -> NoReturn:
        raise argparse.ArgumentError(None, message)

    def error(self, message: str) -> NoReturn:
        usage = self.format_usage()
        error_message = f"{usage}{self.prog}: error: {message}"
        raise argparse.ArgumentError(None, error_message)


@dataclass
class Arg:
    name: str
    variable_name: str = None
    short: str = None
    prefix: str = "--"
    type: any = str
    action: str = None
    const: any = None
    nargs: int = 1
    help: str = ""
    required: bool = None
    default: any = None
    clean_mentions: bool = False

    def __post_init__(self):
        if not self.variable_name:
            self.variable_name = self.name.replace("-", "_")

    def add_to_parser(self, parser):
        arg = dict(self.__dict__)
        del arg["name"]
        del arg["short"]
        del arg["prefix"]
        del arg["clean_mentions"]
        del arg["variable_name"]
        if str(arg["nargs"]).isdigit() and arg["required"] is None:
            arg["required"] = True
        if arg["type"] == bool:
            arg["type"] = str
        if arg["action"]:
            del arg["type"]
            del arg["nargs"]
            if arg["const"] is None:
                del arg["const"]
        if self.prefix == "":
            del arg["required"]

        argument_flags = [f"-{self.short}"] if self.short else []
        argument_flags.append(f"{self.prefix}{self.name}")
        parser.add_argument(*argument_flags, **arg)
        return parser

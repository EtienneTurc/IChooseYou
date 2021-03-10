import argparse
from dataclasses import dataclass

ArgError = argparse.ArgumentError


class ArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        raise argparse.ArgumentError(None, message)

    def error(self, message):
        usage = self.format_usage()
        error_message = f"{usage}{self.prog}: error: {message}"
        raise argparse.ArgumentError(None, error_message)


@dataclass
class Arg:
    name: str
    prefix: str = "--"
    type: any = str
    action: str = None
    const: any = None
    nargs: int = 1
    help: str = ""
    required: bool = None
    default: any = None

    def add_to_parser(self, parser):
        arg = dict(self.__dict__)
        del arg["name"]
        del arg["prefix"]
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
        parser.add_argument(f"{self.prefix}{self.name}", **arg)
        return parser

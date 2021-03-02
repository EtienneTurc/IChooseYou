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
    type: any = str
    action: str = None
    nargs: int = 1
    default: any = None

    def add_to_parser(self, parser, prefix="--"):
        arg = dict(self.__dict__)
        del arg["name"]
        if str(arg["nargs"]).isdigit():
            arg["required"] = True
        if arg["action"]:
            del arg["type"]
            del arg["nargs"]
        parser.add_argument(f"{prefix}{self.name}", **arg)
        return parser

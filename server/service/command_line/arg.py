from dataclasses import dataclass


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
        if arg["type"] == bool:
            arg["type"] = str
        if arg["action"]:
            del arg["type"]
            del arg["nargs"]
            if arg["const"] is None:
                del arg["const"]

        argument_flags = [f"-{self.short}"] if self.short else []
        argument_flags.append(f"{self.prefix}{self.name}")
        parser.add_argument(*argument_flags, **arg)
        return parser

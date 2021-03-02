from server.command.args import ArgumentParser
from server.command.utils import format_text_to_list, options_to_dict


class BaseCommand:
    def __init__(self, text, name="", args=[]):
        self.name = name
        self.args = args

        parser = ArgumentParser(prog=self.name, exit_on_error=False)
        for arg in self.args:
            parser = arg.add_to_parser(parser)

        text_list = format_text_to_list(text)
        options = parser.parse_args(text_list)
        self.options = options_to_dict(options.__dict__, self.args)

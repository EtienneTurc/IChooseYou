from flask import current_app

from server.command.args import Arg, ArgumentParser
from server.command.utils import format_examples, format_text_to_list, options_to_dict


def addHelp(func):
    def _createHelp(self, *args, **kwargs):
        if self.options.get("help"):
            from server.command.help import HelpCommand

            return HelpCommand(self.name, self.channel_id).exec()
        else:
            return func(self, *args, **kwargs)

    return _createHelp


class BaseCommand:
    def __init__(self, text, *, channel_id, description, examples, name="", args=[]):
        self.name = name
        self.description = description
        self.examples = format_examples(
            current_app.config["SLASH_COMMAND"], name, examples
        )
        self.channel_id = channel_id
        self.args = args

        arg_help = Arg(
            name="help",
            short="h",
            nargs=None,
            type=bool,
            action="store_true",
            help="Flag to show help.",
        )

        if text is None:
            return
        text_list = format_text_to_list(text)

        self._parse_args([arg_help], text_list, True)
        if self.options.get("help"):
            return

        self._parse_args(self.args, text_list, False)

    def _parse_args(self, args, text_list, partial=False):
        parser = ArgumentParser(prog=self.name, exit_on_error=False, add_help=False)
        for arg in args:
            arg.add_to_parser(parser)

        if partial:
            options, _ = parser.parse_known_args(text_list)
        else:
            options = parser.parse_args(text_list)

        self.options = options_to_dict(options.__dict__, args)

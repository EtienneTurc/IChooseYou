from flask import current_app

from server.service.command.args import Arg, ArgumentParser
from server.service.command.utils import (
    format_examples,
    format_text_to_list,
    options_to_dict,
)


def addHelp(func):
    def _createHelp(self, *args, **kwargs):
        if self.options.get("help"):
            from server.service.command.help import HelpCommand

            return HelpCommand(
                text=self.name, team_id=self.team_id, channel_id=self.channel_id
            ).exec()
        else:
            return func(self, *args, **kwargs)

    return _createHelp


class BaseCommand:
    def __init__(
        self,
        text: str,
        *,
        team_id: int,
        channel_id: int,
        description: str,
        examples: list[str],
        name: str = "",
        args=[]
    ):
        self.name = name
        self.description = description
        self.examples = format_examples(
            current_app.config["SLASH_COMMAND"], name, examples
        )
        self.channel_id = channel_id
        self.team_id = team_id
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
            parser = self._create_parser([arg_help, *self.args])
            self.usage = parser.format_usage()
            return

        text_list = format_text_to_list(text)

        self._parse_args([arg_help], text_list, True)
        if self.options.get("help"):
            return

        self._parse_args(self.args, text_list, False)

    def _create_parser(self, args):
        parser = ArgumentParser(prog=self.name, exit_on_error=False, add_help=False)
        for arg in args:
            arg.add_to_parser(parser)
        return parser

    def _parse_args(self, args, text_list, partial=False):
        parser = self._create_parser(args)
        if partial:
            options, _ = parser.parse_known_args(text_list)
        else:
            options = parser.parse_args(text_list)

        self.options = options_to_dict(options.__dict__, args)

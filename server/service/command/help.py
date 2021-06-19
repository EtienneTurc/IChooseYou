from server.orm.command import Command
from server.service.command.args import Arg
from server.service.command.base_command import BaseCommand, addHelp
from server.service.command.create import CreateCommand
from server.service.command.delete import DeleteCommand
from server.service.command.update import UpdateCommand
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.message_formatting import (format_custom_command_help,
                                                     format_custom_commands_help,
                                                     format_known_command_help,
                                                     format_known_commands_help)

KNOWN_COMMANDS = {
    "create": CreateCommand,
    "update": UpdateCommand,
    "delete": DeleteCommand,
}


class HelpCommand(BaseCommand):
    def __init__(self, *, text: str, team_id: str, channel_id: str):
        name = "help"
        description = "Command to show commands, args and their values"
        examples = [
            "command_to_get_info_from",
        ]
        args = [
            Arg(
                name="command_name",
                prefix="",
                nargs="?",
                help="Name of the command to show info from. (Optional)",
            ),
        ]
        super(HelpCommand, self).__init__(
            text,
            name=name,
            channel_id=channel_id,
            team_id=team_id,
            description=description,
            examples=examples,
            args=args,
        )

    @addHelp
    def exec(self, *args, **kwargs):
        if self.options.get("command_name"):
            command_name = self.options.get("command_name")
            if command_name in KNOWN_COMMANDS_NAMES:
                command = KNOWN_COMMANDS[command_name]
                return Message(
                    content=format_known_command_help(command),
                    status=MessageStatus.INFO,
                    visibility=MessageVisibility.HIDDEN,
                )

            command = Command.find_one_by_name_and_chanel(command_name, self.channel_id)
            return Message(
                content=format_custom_command_help(command),
                status=MessageStatus.INFO,
                visibility=MessageVisibility.HIDDEN,
            )
        else:
            commands = Command.find_all_in_chanel(self.channel_id)
            return Message(
                content=self._format_commands_help(KNOWN_COMMANDS.values(), commands),
                status=MessageStatus.INFO,
                visibility=MessageVisibility.HIDDEN,
            )

    def _format_commands_help(self, known_commands: list[BaseCommand], custom_commands):
        message_content = "_*Fixed commands:*_\n"
        message_content += format_known_commands_help(known_commands)
        message_content += "\n\n _*Created commands:*_\n"
        message_content += format_custom_commands_help(custom_commands)
        return message_content


KNOWN_COMMANDS["help"] = HelpCommand
KNOWN_COMMANDS_NAMES = KNOWN_COMMANDS.keys()

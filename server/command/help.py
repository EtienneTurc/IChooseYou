from server.command.args import Arg
from server.command.base_command import BaseCommand
from server.command.create import CreateCommand
from server.command.delete import DeleteCommand
from server.command.update import UpdateCommand
from server.orm.command import Command
from server.slack.message_formatting import (
    format_custom_command_help,
    format_custom_commands_help,
    format_known_command_help,
    format_known_commands_help,
)
from server.slack.message_status import MessageStatus

KNOWN_COMMANDS = {
    "create": CreateCommand,
    "update": UpdateCommand,
    "delete": DeleteCommand,
}


class HelpCommand(BaseCommand):
    def __init__(self, text, channel_id):
        self.description = "Command to show commands, args and their values"
        name = "help"
        args = [
            Arg(
                name="commandName",
                nargs="?",
                help="Name of the command to show info from.",
            ),
        ]
        super(HelpCommand, self).__init__(
            text, name=name, channel_id=channel_id, args=args
        )

    def exec(self, *args, **kwargs):
        if self.options.get("commandName"):
            command_name = self.options.get("commandName")
            if command_name in KNOWN_COMMANDS_NAMES:
                command = KNOWN_COMMANDS[command_name]
                return format_known_command_help(command), MessageStatus.INFO

            command = Command.find_one_by_name_and_chanel(command_name, self.channel_id)
            return format_custom_command_help(command), MessageStatus.INFO
        else:
            commands = Command.find_all_in_chanel(self.channel_id)
            return (
                self._format_commands_help(KNOWN_COMMANDS.values(), commands),
                MessageStatus.INFO,
            )

    def _format_commands_help(self, known_commands, custom_commands):
        message = ">*Fixed commands:*\n"
        message += format_known_commands_help(known_commands)
        message += "\n\n> *Created commands:*\n"
        message += format_custom_commands_help(custom_commands)
        return message


KNOWN_COMMANDS["help"] = HelpCommand
KNOWN_COMMANDS_NAMES = KNOWN_COMMANDS.keys()

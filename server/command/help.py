from server.command.args import Arg
from server.command.base_command import BaseCommand, addHelp
from server.command.create import CreateCommand
from server.command.delete import DeleteCommand
from server.command.update import UpdateCommand
from server.orm.command import Command
from server.slack.message_formatting import (format_custom_command_help,
                                             format_custom_commands_help,
                                             format_known_command_help,
                                             format_known_commands_help)
from server.slack.message_status import MessageStatus, MessageVisibility

KNOWN_COMMANDS = {
    "create": CreateCommand,
    "update": UpdateCommand,
    "delete": DeleteCommand,
}


class HelpCommand(BaseCommand):
    def __init__(self, *, text, team_id, channel_id):
        name = "help"
        description = "Command to show commands, args and their values"
        examples = [
            "command_to_get_info_from",
        ]
        args = [
            Arg(
                name="commandName",
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
        if self.options.get("commandName"):
            command_name = self.options.get("commandName")
            if command_name in KNOWN_COMMANDS_NAMES:
                command = KNOWN_COMMANDS[command_name]
                return (
                    format_known_command_help(command),
                    MessageStatus.INFO,
                    MessageVisibility.HIDDEN,
                )

            command = Command.find_one_by_name_and_chanel(command_name, self.channel_id)
            return (
                format_custom_command_help(command),
                MessageStatus.INFO,
                MessageVisibility.HIDDEN,
            )
        else:
            commands = Command.find_all_in_chanel(self.channel_id)
            return (
                self._format_commands_help(KNOWN_COMMANDS.values(), commands),
                MessageStatus.INFO,
                MessageVisibility.HIDDEN,
            )

    def _format_commands_help(self, known_commands, custom_commands):
        message = "_*Fixed commands:*_\n"
        message += format_known_commands_help(known_commands)
        message += "\n\n _*Created commands:*_\n"
        message += format_custom_commands_help(custom_commands)
        return message


KNOWN_COMMANDS["help"] = HelpCommand
KNOWN_COMMANDS_NAMES = KNOWN_COMMANDS.keys()

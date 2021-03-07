from server.command.args import Arg, ArgError
from server.command.base_command import BaseCommand
from server.orm.command import Command
from server.slack.message_status import MessageStatus


class DeleteCommand(BaseCommand):
    def __init__(self, text, channel_id):
        self.description = "Delete a given command"
        name = "delete"
        args = [
            Arg(
                name="commandName",
                nargs=1,
                help="Name of the command to delete.",
            ),
        ]
        super(DeleteCommand, self).__init__(
            text, name=name, channel_id=channel_id, args=args
        )

    def exec(self, *args, **kwargs):
        command_name = self.options.get("commandName")

        try:
            command = Command.find_one_by_name_and_chanel(command_name, self.channel_id)
        except Command.DoesNotExist:
            raise ArgError(None, f"Command {command_name} does not exist.")

        Command.delete(command)

        message = f"Command {command_name} successfully deleted."
        return message, MessageStatus.INFO

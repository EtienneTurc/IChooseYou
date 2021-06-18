from server.orm.command import Command
from server.service.command.args import Arg
from server.service.command.base_command import BaseCommand, addHelp
from server.service.slack.message import (
    Message,
    MessageStatus,
    MessageVisibility,
)


class DeleteCommand(BaseCommand):
    def __init__(self, *, text, team_id, channel_id):
        name = "delete"
        description = "Delete a given command"
        examples = [
            "my_command_to_delete",
        ]
        args = [
            Arg(
                name="commandName",
                prefix="",
                nargs=1,
                help="Name of the command to delete.",
            ),
        ]
        super(DeleteCommand, self).__init__(
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
        command_name = self.options.get("commandName")
        command = Command.find_one_by_name_and_chanel(command_name, self.channel_id)
        Command.delete_command(command)

        message_content = f"Command {command_name} successfully deleted."
        return Message(
            content=message_content,
            status=MessageStatus.INFO,
            visibility=MessageVisibility.NORMAL,
        )

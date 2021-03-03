from server.command.base_command import BaseCommand
from server.command.args import Arg, ArgError
from server.orm.command import Command
from server.slack.message_formatting import (
    format_custom_command_help,
)


class UpdateCommand(BaseCommand):
    def __init__(self, text, channel_id):
        self.description = "Update a given command"
        name = "update"
        args = [
            Arg(
                name="commandName",
                nargs=1,
                help="Name of the command to update.",
            ),
            Arg(name="label", nargs="*", help="New label"),
            Arg(name="pickList", nargs="*", type=list, help="New pick list"),
            Arg(
                name="addToPickList",
                nargs="*",
                type=list,
                help="Elements to add to the pick list.",
            ),
            Arg(
                name="removeFromPickList",
                nargs="*",
                type=list,
                help="Elements to remove from the pick list.",
            ),
            Arg(
                name="selfExclude",
                nargs="?",
                default=False,
                help="Exclude the person using the slash command to be picked.",
            ),
        ]
        super(UpdateCommand, self).__init__(
            text, name=name, channel_id=channel_id, args=args
        )

    def exec(self):
        command_name = self.options.get("commandName")
        command = Command.find_one_by_name_and_chanel(command_name, self.channel_id)

        if not command:
            raise ArgError(None, f"Command {command_name} does not exist.")

        new_values = {}
        if self.options.ge("label"):
            new_values["label"] = self.options.ge("label")

        if self.options.get("addToPickList"):
            new_values["pickList"] = list(
                set(command.pickList) + set(self.options.get("addToPickList"))
            )

        if self.options.get("removeFromPickList"):
            pickList = (
                new_values.get("pickList")
                if new_values.get("pickList")
                else command.pickList
            )
            new_values["pickList"] = list(
                set(pickList) + set(self.options.get("addToPickList"))
            )

        if self.options.get("pickList"):
            new_values["pickList"] = self.options.get("pickList")

        if self.options.get("selfExclude"):
            new_values["selfExclude"] = self.options.get("selfExclude")

        Command.update(command, new_values)

        updated_command = Command.find_one_by_name_and_chanel(
            command_name, self.channel_id
        )

        message = f"Command {updated_command.name} successfully updated.\n"
        message += format_custom_command_help(updated_command)
        return message

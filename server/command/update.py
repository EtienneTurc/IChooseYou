from server.command.base_command import BaseCommand
from server.command.args import Arg, ArgError
from server.orm.command import Command
from server.slack.message_formatting import (
    format_custom_command_help,
)
from server.slack.message_status import MessageStatus


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
                const="True",
                type=bool,
                help="Exclude the person using the slash command to be picked.",
            ),
        ]
        super(UpdateCommand, self).__init__(
            text, name=name, channel_id=channel_id, args=args
        )

    def exec(self):
        command_name = self.options["commandName"]
        command = Command.find_one_by_name_and_chanel(command_name, self.channel_id)

        if not command:
            raise ArgError(None, f"Command {command_name} does not exist.")

        new_values = {}
        if self.options["label"]:
            new_values["label"] = self.options["label"]

        if self.options["addToPickList"]:
            new_values["pick_list"] = list(
                set(command.pick_list) | set(self.options["addToPickList"])
            )

        if self.options["removeFromPickList"]:
            pick_list = (
                new_values.get("pick_list")
                if new_values.get("pick_list")
                else command.pick_list
            )
            new_values["pick_list"] = list(
                set(pick_list) - set(self.options["removeFromPickList"])
            )

        if self.options["pickList"]:
            new_values["pick_list"] = self.options["pickList"]

        if self.options["selfExclude"] is not None:
            new_values["self_exclude"] = self.options["selfExclude"]

        print(self.options)
        print(bool(self.options["selfExclude"]))
        print(new_values)
        Command.update(command.name, command.channel_id, new_values)

        updated_command = Command.find_one_by_name_and_chanel(
            command_name, self.channel_id
        )

        message = f"Command {updated_command.name} successfully updated.\n"
        message += format_custom_command_help(updated_command)
        return message, MessageStatus.SUCCESS

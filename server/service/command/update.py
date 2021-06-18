from server.orm.command import Command
from server.service.command.args import Arg
from server.service.command.base_command import BaseCommand, addHelp
from server.service.command.utils import format_pick_list
from server.service.slack.message_formatting import format_custom_command_help
from server.service.slack.message import (
    Message,
    MessageStatus,
    MessageVisibility,
)


class UpdateCommand(BaseCommand):
    def __init__(self, *, text, team_id, channel_id):
        name = "update"
        description = "Update a given command"
        examples = [
            "mySuperCommand --addToPickList my_element_to_add",
            "mySuperCommand --pickList my new pick list",
            "mySuperCommand --selfExclude",
        ]
        args = [
            Arg(
                name="commandName",
                prefix="",
                nargs=1,
                help="Name of the command to update.",
            ),
            Arg(name="label", short="l", nargs="*", help="New label"),
            Arg(
                name="pickList",
                short="p",
                nargs="*",
                type=list,
                clean_mentions=True,
                help="New pick list",
            ),
            Arg(
                name="addToPickList",
                short="a",
                nargs="*",
                type=list,
                clean_mentions=True,
                help="Elements to add to the pick list.",
            ),
            Arg(
                name="removeFromPickList",
                short="r",
                nargs="*",
                type=list,
                clean_mentions=True,
                help="Elements to remove from the pick list.",
            ),
            Arg(
                name="selfExclude",
                short="s",
                nargs="?",
                const="True",
                type=bool,
                help="Exclude the person using the slash command to be picked.",
            ),
        ]
        super(UpdateCommand, self).__init__(
            text,
            name=name,
            channel_id=channel_id,
            team_id=team_id,
            description=description,
            examples=examples,
            args=args,
        )

    @addHelp
    def exec(self, user_id, *args, **kwargs):
        command_name = self.options["commandName"]
        command = Command.find_one_by_name_and_chanel(command_name, self.channel_id)

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
            new_values["pick_list"] = format_pick_list(
                self.options["pickList"], self.team_id, self.channel_id
            )

        if self.options["selfExclude"] is not None:
            new_values["self_exclude"] = self.options["selfExclude"]

        Command.update(command.name, command.channel_id, user_id, new_values)

        updated_command = Command.find_one_by_name_and_chanel(
            command_name, self.channel_id
        )

        message_content = f"Command {updated_command.name} successfully updated.\n"
        message_content += format_custom_command_help(updated_command)
        return Message(
            content=message_content,
            status=MessageStatus.SUCCESS,
            visibility=MessageVisibility.NORMAL,
        )

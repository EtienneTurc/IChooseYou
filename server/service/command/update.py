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
    def __init__(self, *, text: str, team_id: int, channel_id: int):
        name = "update"
        description = "Update a given command"
        examples = [
            "mySuperCommand --add-to-pick-list my_element_to_add",
            "mySuperCommand --pick-list my new pick list",
            "mySuperCommand --self-exclude --only-active-users",
        ]
        args = [
            Arg(
                name="command_name",
                prefix="",
                nargs=1,
                help="Name of the command to update.",
            ),
            Arg(name="label", short="l", nargs="*", help="New label"),
            Arg(
                name="pick-list",
                short="p",
                nargs="*",
                type=list,
                clean_mentions=True,
                help="New pick list",
            ),
            Arg(
                name="add-to-pick-list",
                short="a",
                nargs="*",
                type=list,
                clean_mentions=True,
                help="Elements to add to the pick list.",
            ),
            Arg(
                name="remove-from-pick-list",
                short="r",
                nargs="*",
                type=list,
                clean_mentions=True,
                help="Elements to remove from the pick list.",
            ),
            Arg(
                name="self-exclude",
                short="s",
                nargs="?",
                const="True",
                type=bool,
                help="Exclude the person using the slash command to be picked.",
            ),
            Arg(
                name="only-active-users",
                short="o",
                nargs="?",
                const="True",
                type=bool,
                help="Exclude non active users to be picked.",
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
    def exec(self, user_id: int, *args, **kwargs) -> Message:
        command_name = self.options["command_name"]
        command = Command.find_one_by_name_and_chanel(command_name, self.channel_id)

        new_values = {}
        if self.options["label"]:
            new_values["label"] = self.options["label"]

        if self.options["add_to_pick_list"]:
            new_values["pick_list"] = list(
                set(command.pick_list) | set(self.options["add_to_pick_list"])
            )

        if self.options["remove_from_pick_list"]:
            pick_list = (
                new_values.get("pick_list")
                if new_values.get("pick_list")
                else command.pick_list
            )
            new_values["pick_list"] = list(
                set(pick_list) - set(self.options["remove_from_pick_list"])
            )

        if self.options["pick_list"]:
            new_values["pick_list"] = format_pick_list(
                self.options["pick_list"], self.team_id, self.channel_id
            )

        if self.options["self_exclude"] is not None:
            new_values["self_exclude"] = self.options["self_exclude"]

        if self.options["only_active_users"] is not None:
            new_values["only_active_users"] = self.options["only_active_users"]

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

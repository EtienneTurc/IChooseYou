from server.orm.command import Command
from server.service.command.args import Arg
from server.service.command.base_command import BaseCommand, addHelp
from server.service.command.enum import PickListSpecialArg
from server.service.command.utils import format_pick_list
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.message_formatting import format_custom_command_help

label_help = "Text to display using the following format:"
label_help += "\n>Hey ! <user> choose <element> to <your_label> <text_on_call>\n"


pick_list_help = "List from which to pick from."
pick_list_help += " Elements must be separated by spaces,"
pick_list_help += " thus an element can't be composed of two words."
pick_list_help += "\n> If you want to directly notify a user when he is selected,"
pick_list_help += " you must mention him in the pickList."
pick_list_help += "\n> You can add all members of the channel to the pick list"
pick_list_help += f" with the argument `-p {PickListSpecialArg.ALL_MEMBERS.value}`"
pick_list_help += f" or `--pick-list {PickListSpecialArg.ALL_MEMBERS.value}`."


class CreateCommand(BaseCommand):
    def __init__(self, *, text: str, team_id: int, channel_id: int) -> None:
        name = "create"
        description = "Command to create new slash commands"
        examples = [
            "mySuperCommand --pick-list first_element second --label my super awesome label",  # noqa E501
            f"mySuperCommand --pick-list {PickListSpecialArg.ALL_MEMBERS.value} --label will add members of the channel",  # noqa E501
        ]

        args = [
            Arg(
                name="command_name",
                prefix="",
                nargs=1,
                help="Name of the command to create.",
            ),
            Arg(name="label", short="l", nargs="+", required=True, help=label_help),
            Arg(
                name="pick-list",
                short="p",
                nargs="+",
                required=True,
                clean_mentions=True,
                type=list,
                help=pick_list_help,
            ),
            Arg(
                name="self-exclude",
                short="s",
                nargs="?",
                const="True",
                default="False",
                type=bool,
                help="Exclude the person using the slash command to be picked. Default value is False.",  # noqa E501
            ),
            Arg(
                name="only-active-users",
                short="o",
                nargs="?",
                const="True",
                default="False",
                type=bool,
                help="Exclude non active users to be picked. Default value is False.",
            ),
        ]
        super(CreateCommand, self).__init__(
            text,
            name=name,
            description=description,
            examples=examples,
            channel_id=channel_id,
            team_id=team_id,
            args=args,
        )

    @addHelp
    def exec(self, user_id: int, *args, **kwargs) -> Message:
        pick_list = format_pick_list(
            self.options["pick_list"], self.team_id, self.channel_id
        )
        print(self.options)

        Command.create(
            name=self.options["command_name"],
            channel_id=self.channel_id,
            label=self.options["label"],
            pick_list=pick_list,
            self_exclude=self.options["self_exclude"],
            only_active_users=self.options["only_active_users"],
            created_by_user_id=user_id,
        )
        created_command = Command.find_one_by_name_and_chanel(
            self.options["command_name"], self.channel_id
        )
        message_content = f"Command {created_command.name} successfully created.\n"
        message_content += format_custom_command_help(created_command)
        return Message(
            content=message_content,
            status=MessageStatus.SUCCESS,
            visibility=MessageVisibility.NORMAL,
        )

from server.command.args import Arg
from server.command.base_command import BaseCommand, addHelp
from server.command.utils import format_pick_list
from server.command.validator import assert_label_is_correct
from server.orm.command import Command
from server.slack.message_formatting import format_custom_command_help
from server.slack.message_status import MessageStatus, MessageVisibility

label_help = "Text to display using the following format:"
label_help += "\n>Hey ! <user> choose <element> to <your_label>\n"
label_help += " Note that you can parametrize your label with args from the"
label_help += " command line with $1 ... $N for positional arguments"
label_help += " or with $name_of_my_arg for named arguments.\n"
label_help += " For instance 'my label with $1 positional argument and"
label_help += " a named argument named $name' is a valid label with two arguments."


pick_list_help = "List from which to pick from."
pick_list_help += " Elements must be separated by spaces,"
pick_list_help += " thus an element can't be composed of two words."
pick_list_help += "\n> If you want to directly notify a user when he is selected,"
pick_list_help += " you must mention him in the pickList."
pick_list_help += "\n> You can add all members of the channel to the pick list"
pick_list_help += " with the argument `-p all_members` or `--pickList all_members`."


class CreateCommand(BaseCommand):
    def __init__(self, text, channel_id):
        name = "create"
        description = "Command to create new slash commands"
        examples = [
            "mySuperCommand --pickList first_element second --label my super awesome label",  # noqa E501
            "mySuperCommand --pickList all_members --label will replace bash args such as $1 or $my_var_name",  # noqa E501
        ]

        args = [
            Arg(
                name="commandName",
                prefix="",
                nargs=1,
                help="Name of the command to create.",
            ),
            Arg(name="label", short="l", nargs="+", required=True, help=label_help),
            Arg(
                name="pickList",
                short="p",
                nargs="+",
                required=True,
                clean_mentions=True,
                type=list,
                help=pick_list_help,
            ),
            Arg(
                name="selfExclude",
                short="s",
                nargs="?",
                const="True",
                default="False",
                type=bool,
                help="Exclude the person using the slash command to be picked. Default value is False.",  # noqa E501
            ),
        ]
        super(CreateCommand, self).__init__(
            text,
            name=name,
            description=description,
            examples=examples,
            channel_id=channel_id,
            args=args,
        )

    @addHelp
    def exec(self, user_id, *args, **kwargs):
        assert_label_is_correct(self.options["label"])

        pick_list = format_pick_list(self.options["pickList"], self.channel_id)

        Command.create(
            self.options["commandName"],
            self.channel_id,
            self.options["label"],
            pick_list,
            self.options["selfExclude"],
            user_id,
        )
        created_command = Command.find_one_by_name_and_chanel(
            self.options["commandName"], self.channel_id
        )
        message = f"Command {created_command.name} successfully created.\n"
        message += format_custom_command_help(created_command)
        return message, MessageStatus.SUCCESS, MessageVisibility.NORMAL

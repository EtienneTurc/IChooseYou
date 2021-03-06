from server.command.args import Arg
from server.command.base_command import BaseCommand
from server.command.validator import assert_label_is_correct
from server.orm.command import Command
from server.slack.message_formatting import format_custom_command_help
from server.slack.message_status import MessageStatus

label_help = "*Text to display using the following format*:"
label_help += "\n>Hey ! <user> choose <element> to <your_label>\n"
label_help += " Note that you can use parametrize your label with args from the"
label_help += " command line with $1 ... $N for positional arguments"
label_help += " or with $name_of_my_arg for named arguments.\n"
label_help += " For instance 'my label with $1 positional argument and"
label_help += " a named argument named $name' is a valid label with two arguments."


pick_list_help = "*List from which to pick from*."
pick_list_help += " Elements must be separated by *spaces*,"
pick_list_help += " thus an element can't be composed of two words."
pick_list_help += "\n> If you want to directly notify a user when he is selected,"
pick_list_help += " you must mention him in the pickList."


class CreateCommand(BaseCommand):
    def __init__(self, text, channel_id):
        self.description = "Command to create new slash commands"
        name = "create"
        args = [
            Arg(name="commandName", nargs=1, help="Name of the command to create."),
            Arg(name="label", nargs="+", required=True, help=label_help),
            Arg(
                name="pickList",
                nargs="+",
                required=True,
                type=list,
                help=pick_list_help,
            ),
            Arg(
                name="selfExclude",
                nargs="?",
                const="True",
                default="False",
                type=bool,
                help="Exclude the person using the slash command to be picked.",
            ),
            Arg(name="quiet", nargs="?", default=False, help="Silence"),
        ]
        super(CreateCommand, self).__init__(
            text, name=name, channel_id=channel_id, args=args
        )

    def exec(self):
        assert_label_is_correct(self.options["label"])
        Command.create(
            self.options["commandName"],
            self.channel_id,
            self.options["label"],
            self.options["pickList"],
            self.options["selfExclude"],
        )
        created_command = Command.find_one_by_name_and_chanel(
            self.options["commandName"], self.channel_id
        )
        message = f"Command {created_command.name} successfully created.\n"
        message += format_custom_command_help(created_command)
        return message, MessageStatus.SUCCESS

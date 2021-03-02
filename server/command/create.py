from server.command.args import Arg
from server.command.base_command import BaseCommand
from server.command.validator import assert_label_is_correct
from server.orm import Command


class CreateCommand(BaseCommand):
    def __init__(self, text):
        name = "create"
        args = [
            Arg(name="name", nargs=1),
            Arg(name="label", nargs="+"),
            Arg(name="pickList", nargs="+", type=list),
            Arg(name="selfExclude", nargs="?", default=False),
            Arg(name="quiet", nargs="?", default=False),
        ]
        super(CreateCommand, self).__init__(text, name=name, args=args)

    def exec(self):
        assert_label_is_correct(self.options["label"])
        Command.create(
            self.options["name"],
            self.options["label"],
            self.options["pickList"],
            self.options["selfExclude"],
        )

        # quiet = options.get("quiet")

        # if not quiet:
        #     quiet = self.args.quiet.default

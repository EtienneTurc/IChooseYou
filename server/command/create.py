from .args import Arg
from ..orm import Command
from .base_command import BaseCommand
from .utils import assert_label_is_correct, get_as_string, get_as_bool, get_as_list


class CreateCommand(BaseCommand):
    name = "create"
    args = {
        "command_name": Arg(name="name", nargs=1),
        "label": Arg(name="label", nargs="+"),
        "pick_list": Arg(name="pickList", nargs=1),
        "self_exclude": Arg(name="selfExclude", nargs="?", default=False),
        "quiet": Arg(name="quiet", nargs="?", default=False),
    }

    def exec(self, text):
        options = super().exec(text)

        label = get_as_string(options, "label")

        assert_label_is_correct(label)
        Command.create(
            get_as_string(options, "name"),
            label,
            get_as_list(options, "pickList"),
            get_as_bool(options, "selfExclude"),
        )

        # quiet = options.get("quiet")

        # if not quiet:
        #     quiet = self.args.quiet.default

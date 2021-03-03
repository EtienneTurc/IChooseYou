import pytest

from server.command.args import Arg, ArgError
from server.command.base_command import BaseCommand

name = "test_base_command"
channel_id = "42"
first_args = Arg(name="first_args", nargs=1)
multiple_args = Arg(name="multiple_args", nargs="+")
list_args = Arg(name="list_args", nargs="+", type=list)
bool_arg = Arg(
    name="bool_arg", nargs="?", type=bool, action="store_true", default=False
)


@pytest.mark.parametrize(
    "text, args, expected_options",
    [
        (
            "--first_args hello",
            [first_args],
            {"first_args": "hello"},
        ),
        (
            "--multiple_args hello world",
            [multiple_args],
            {"multiple_args": "hello world"},
        ),
        (
            "--list_args hello world",
            [list_args],
            {"list_args": ["hello", "world"]},
        ),
        (
            "--bool_arg",
            [bool_arg],
            {"bool_arg": True},
        ),
        (
            "--list_args hello world",
            [list_args, bool_arg],
            {"list_args": ["hello", "world"], "bool_arg": False},
        ),
        (
            "",
            [bool_arg],
            {"bool_arg": False},
        ),
        (
            " ",
            [bool_arg],
            {"bool_arg": False},
        ),
        (
            "--multiple_args hello  ",
            [multiple_args],
            {"multiple_args": "hello  "},
        ),
    ],
)
def test_base_command_init(text, args, expected_options):
    options = BaseCommand(text, name, channel_id, args).options
    for key in expected_options:
        assert options[key] == expected_options[key]


@pytest.mark.parametrize(
    "text, args",
    [
        (
            "",
            [first_args],
        ),
        (
            "--first_args",
            [first_args],
        ),
        (
            "--first_args hello hello",
            [first_args],
        ),
        (
            "--multiple_args hello",
            [first_args],
        ),
    ],
)
def test_base_command_init_raise_error(text, args):
    with pytest.raises(ArgError):
        BaseCommand(text, name, channel_id, args)

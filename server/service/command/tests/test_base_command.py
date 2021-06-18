import pytest

from server.service.command.args import Arg, ArgError
from server.service.command.base_command import BaseCommand
from server.tests.test_app import *  # noqa: F401, F403

name = "test_base_command"
team_id = "1337"
channel_id = "42"
description = "My super description"
examples = ["whatever"]
first_args = Arg(name="first_args", nargs=1)
multiple_args = Arg(name="multiple_args", nargs="+")
list_args = Arg(name="list_args", nargs="+", type=list)
bool_arg = Arg(
    name="bool_arg", nargs="?", type=bool, action="store_true", default=False
)
optional_single_arg = Arg(name="optional_single_arg", nargs="?")


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
        (
            "--optional_single_arg hello",
            [optional_single_arg],
            {"optional_single_arg": "hello"},
        ),
    ],
)
def test_base_command_init(text, args, expected_options, client):
    options = BaseCommand(
        text,
        name=name,
        description=description,
        examples=examples,
        channel_id=channel_id,
        team_id=team_id,
        args=args,
    ).options
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
        (
            "--optional_single_arg hello world",
            [optional_single_arg],
        ),
    ],
)
def test_base_command_init_raise_error(text, args, client):
    with pytest.raises(ArgError):
        BaseCommand(
            text,
            name=name,
            description=description,
            examples=examples,
            channel_id=channel_id,
            team_id=team_id,
            args=args,
        )

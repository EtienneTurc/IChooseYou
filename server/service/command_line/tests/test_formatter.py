import pytest

from server.service.command_line.arg import Arg
from server.service.command_line.formatter import parse_command_line

positional_first_arg = Arg(name="positional_first_arg", nargs=1)
positional_second_arg = Arg(name="positional_second_arg", nargs=1)
simple_named_arg = Arg(name="simple_named_arg", nargs=1)
multiple_args = Arg(name="multiple_args", nargs="+")
list_args = Arg(name="list_args", nargs="+", type=list)
bool_arg = Arg(
    name="bool_arg", nargs="?", type=bool, action="store_true", default=False
)
optional_single_arg = Arg(name="optional_single_arg", nargs="?")


@pytest.mark.parametrize(
    "text, positional_args, named_args, expected",
    [
        (
            "hello",
            [positional_first_arg],
            [],
            {"positional_first_arg": "hello"},
        ),
        (
            "hello",
            [],
            [],
            {},
        ),
        (
            "hello world",
            [positional_first_arg],
            [],
            {"positional_first_arg": "hello"},
        ),
        (
            "hello world",
            [positional_first_arg, positional_second_arg],
            [],
            {"positional_first_arg": "hello", "positional_second_arg": "world"},
        ),
        (
            "",
            [positional_first_arg],
            [],
            {},
        ),
        (
            "",
            [positional_first_arg, positional_second_arg],
            [],
            {},
        ),
        (
            "--simple_named_arg hello",
            [],
            [simple_named_arg],
            {"simple_named_arg": "hello"},
        ),
        (
            "--simple_named_arg hello",
            [],
            [simple_named_arg, multiple_args],
            {"simple_named_arg": "hello", "multiple_args": ""},
        ),
        (
            "--multiple_args hello world",
            [],
            [multiple_args],
            {"multiple_args": "hello world"},
        ),
        (
            "--list_args hello world",
            [],
            [list_args],
            {"list_args": ["hello", "world"]},
        ),
        (
            "--bool_arg",
            [],
            [bool_arg],
            {"bool_arg": True},
        ),
        (
            "--list_args hello world",
            [],
            [list_args, bool_arg],
            {"list_args": ["hello", "world"]},
        ),
        (
            "",
            [],
            [bool_arg],
            {},
        ),
        (
            "--multiple_args hello  ",
            [],
            [multiple_args],
            {"multiple_args": "hello  "},
        ),
        (
            "--optional_single_arg hello",
            [],
            [optional_single_arg],
            {"optional_single_arg": "hello"},
        ),
        (
            "hello --simple_named_arg world",
            [positional_first_arg],
            [simple_named_arg],
            {"positional_first_arg": "hello", "simple_named_arg": "world"},
        ),
        (
            "hello --simple_named_arg world --multiple_args to all",
            [positional_first_arg],
            [simple_named_arg, multiple_args],
            {
                "positional_first_arg": "hello",
                "simple_named_arg": "world",
                "multiple_args": "to all",
            },
        ),
    ],
)
def test_parse_command_line(text, positional_args, named_args, expected):
    response = parse_command_line(text, positional_args, named_args)
    for key in expected:
        assert response[key] == expected[key]

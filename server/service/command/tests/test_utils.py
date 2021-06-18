import pytest

from server.service.command.args import Arg
from server.service.command.utils import find_args_in_text, get_args_in_label


@pytest.mark.parametrize(
    "text, expected_positional_args, expected_named_args",
    [
        (
            "first_args --name value",
            [Arg(name="first_args")],
            [Arg(name="name", nargs="+")],
        ),
        (
            "--name value",
            [],
            [Arg(name="name", nargs="+")],
        ),
        (
            "first_args",
            [Arg(name="first_args")],
            [],
        ),
        (
            "",
            [],
            [],
        ),
    ],
)
def test_find_args_in_text(text, expected_positional_args, expected_named_args):
    res_pos_args, res_named_args = find_args_in_text(text)
    assert res_pos_args == expected_positional_args
    assert res_named_args == expected_named_args


@pytest.mark.parametrize(
    "label, expected_positional_args, expected_named_args",
    [
        ("$1", ["$1"], []),
        ("$2", ["$2"], []),
        ("$1 $1", ["$1", "$1"], []),
        ("$1 $3", ["$1", "$3"], []),
        ("$3 $1", ["$3", "$1"], []),
        ("$name", [], ["$name"]),
        ("$name $name", [], ["$name", "$name"]),
        ("$name $dollar", [], ["$name", "$dollar"]),
        ("$1 and $name $dollar", ["$1"], ["$name", "$dollar"]),
    ],
)
def test_get_args_in_label(label, expected_positional_args, expected_named_args):
    res_pos_args, res_named_args = get_args_in_label(label)
    assert res_pos_args == expected_positional_args
    assert res_named_args == expected_named_args

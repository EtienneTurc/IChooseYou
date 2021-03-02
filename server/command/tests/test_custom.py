import pytest

from server.command.args import ArgError
from server.command.custom import CustomCommand

name = "custom_command"
pick_list = [1, 2, 3]
self_exclude = False


@pytest.mark.parametrize(
    "label, args_text, expected_label",
    [
        (
            "Hello $1",
            "world",
            "Hello world",
        ),
        (
            "Hello $world",
            "--world World is wonderful",
            "Hello World is wonderful",
        ),
        (
            "I am $1 and $1",
            "here",
            "I am here and here",
        ),
        (
            "I am $h and $h",
            "--h here",
            "I am here and here",
        ),
        (
            "I am $1 and $2",
            "here there",
            "I am here and there",
        ),
        (
            "I am $1 and $2 but not $ot",
            "here there --ot over there",
            "I am here and there but not over there",
        ),
    ],
)
def test_create_label(label, args_text, expected_label):
    custom_command = CustomCommand(name, label, pick_list, self_exclude)
    assert custom_command._create_label(args_text) == expected_label


@pytest.mark.parametrize(
    "label, args_text",
    [
        (
            "Hello",
            "world",
        ),
        (
            "Hello $world",
            "--world",
        ),
        (
            "Hello",
            "--world",
        ),
        (
            "Hello $world",
            "",
        ),
        (
            "Hello $1",
            "",
        ),
        (
            "Hello $1 $world",
            "--world World",
        ),
    ],
)
def test_create_label_raise_error(label, args_text):
    custom_command = CustomCommand(name, label, pick_list, self_exclude)
    with pytest.raises(ArgError):
        custom_command._create_label(args_text)

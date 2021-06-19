import pytest

from server.service.command.args import ArgError
from server.service.command.custom import CustomCommand

name = "custom_command"
pick_list = [1, 2, 3]
self_exclude = False
only_active_users = False


@pytest.mark.parametrize(
    "label, text, expected_label",
    [
        (
            "",
            "",
            "",
        ),
        (
            "",
            "world",
            "world",
        ),
        (
            "Hello",
            "",
            "Hello",
        ),
        (
            "Hello",
            "world",
            "Hello world",
        ),
        (
            "Hello",
            "world is wonderful",
            "Hello world is wonderful",
        ),
        (
            "I am here",
            "",
            "I am here",
        ),
    ],
)
def test_create_label(label, text, expected_label):
    custom_command = CustomCommand(
        name=name,
        label=label,
        pick_list=pick_list,
        self_exclude=False,
        only_active_users=False,
    )
    assert custom_command._create_label(text) == expected_label


def test_custom_command():
    custom_command = CustomCommand(
        name=name,
        label="my fancy label",
        pick_list=pick_list,
        self_exclude=False,
        only_active_users=False,
    )
    message = custom_command.exec(4321, "")
    assert "Hey ! <@4321> choose " in message.content
    assert "my fancy label" in message.content


def test_custom_command_self_exclude():
    custom_command = CustomCommand(
        name=name,
        label="my label",
        pick_list=["<@4321|name>", "2"],
        self_exclude=True,
        only_active_users=False,
    )
    message = custom_command.exec(4321, "")
    assert "choose 2" in message.content


def test_custom_command_self_exclude_error():
    custom_command = CustomCommand(
        name=name,
        label="my label",
        pick_list=["<@4321|name>"],
        self_exclude=True,
        only_active_users=False,
    )
    error_message = "Pick list contains only the user using the command.*selfExclude.*True.*"  # noqa E501
    with pytest.raises(ArgError, match=error_message):
        custom_command.exec(4321, "")


def test_custom_command_pick_list_empty():
    custom_command = CustomCommand(
        name=name,
        label="my label",
        pick_list=[],
        self_exclude=False,
        only_active_users=False,
    )
    error_message = "Can't pick an element from an empty pick list."
    with pytest.raises(ArgError, match=error_message):
        custom_command.exec(4321, "")

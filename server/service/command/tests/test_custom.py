import pytest

import server.service.slack.tests.monkey_patch as monkey_patch_request  # noqa: F401, E501
from server.service.command.args import ArgError
from server.service.command.custom import CustomCommand
from server.service.error.back_error import BackError
from server.service.strategy.enum import Strategy
from server.tests.test_app import *  # noqa: F401, F403
from server.tests.test_fixture import *  # noqa: F401, F403

name = "custom_command"
pick_list = ["1", "2", "3"]
weight_list = [1 / 3, 1 / 3, 1 / 3]
strategy = Strategy.uniform.name
self_exclude = False
only_active_users = False
user_id = "4321"


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
        weight_list=weight_list,
        strategy=strategy,
        self_exclude=False,
        only_active_users=False,
        text=text,
    )
    assert custom_command._create_label() == expected_label


def test_custom_command():
    custom_command = CustomCommand(
        name=name,
        label="my fancy label",
        pick_list=pick_list,
        weight_list=weight_list,
        strategy=strategy,
        self_exclude=False,
        only_active_users=False,
        text="",
    )
    message, _ = custom_command.exec(user_id)
    assert "Hey ! <@4321> choose " in message.content
    assert "my fancy label" in message.content


def test_custom_command_self_exclude():
    custom_command = CustomCommand(
        name=name,
        label="my label",
        pick_list=["<@4321|name>", "2"],
        weight_list=[1 / 2, 1 / 2],
        strategy=strategy,
        self_exclude=True,
        only_active_users=False,
        text="",
    )
    message, [selected_item] = custom_command.exec(user_id)
    assert "choose 2" in message.content
    assert selected_item == "2"


def test_custom_command_self_exclude_error():
    custom_command = CustomCommand(
        name=name,
        label="my label",
        pick_list=["<@4321|name>"],
        weight_list=[1],
        strategy=strategy,
        self_exclude=True,
        only_active_users=False,
        text="",
    )
    error_message = "Pick list contains only the user using the command.*selfExclude.*True.*"  # noqa E501
    with pytest.raises(ArgError, match=error_message):
        custom_command.exec(user_id)


def test_custom_command_pick_list_empty():
    custom_command = CustomCommand(
        name=name,
        label="my label",
        pick_list=[],
        weight_list=[],
        strategy=strategy,
        self_exclude=False,
        only_active_users=False,
        text="",
    )
    error_message = "Can't pick an item from an empty pick list."
    with pytest.raises(BackError, match=error_message):
        custom_command.exec(user_id)


def test_custom_only_active_users(client):
    custom_command = CustomCommand(
        name=name,
        label="my label",
        pick_list=["<@1234|name>"],
        weight_list=[1],
        strategy=strategy,
        self_exclude=False,
        only_active_users=True,
        text="",
    )
    message, [selected_item] = custom_command.exec(user_id)
    assert "<@1234|name>" in message.content
    assert selected_item == "<@1234|name>"


def test_custom_only_active_users_error(client):
    custom_command = CustomCommand(
        name=name,
        label="my label",
        pick_list=["<@4321|name>"],
        weight_list=[1],
        strategy=strategy,
        self_exclude=False,
        only_active_users=True,
        text="",
    )
    error_message = "No active users to select found."
    with pytest.raises(BackError, match=error_message):
        custom_command.exec(user_id)


@pytest.mark.parametrize(
    "label, text, expected_message",
    [
        (
            "",
            "",
            "choose 1",
        ),
        (
            "",
            "-n 1",
            "choose 1",
        ),
        (
            "",
            "--number-of-items-to-select 1",
            "choose 1",
        ),
        (
            "",
            "--number-of-items-to-select 2",
            "choose 1 and 3",
        ),
        (
            "",
            "-n 3",
            "choose 1, 3 and 2",
        ),
        (
            "my label",
            "-n 2 custom text",
            "choose 1 and 3 my label custom text",
        ),
        (
            "my label",
            "custom text -n 2",
            "choose 1 and 3 my label custom text",
        ),
    ],
)
def test_custom_command_multi_select(label, text, expected_message, set_seed):
    custom_command = CustomCommand(
        name=name,
        label=label,
        pick_list=pick_list,
        weight_list=weight_list,
        strategy=strategy,
        self_exclude=False,
        only_active_users=False,
        text=text,
    )
    message, _ = custom_command.exec(user_id)
    assert expected_message in message.content
    assert " -n " not in message.content
    assert " --number-of-items-to-select " not in message.content

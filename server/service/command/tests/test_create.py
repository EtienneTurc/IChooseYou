import pytest

import server.service.slack.tests.monkey_patch as monkey_patch_request  # noqa: F401, E501
from server.service.command.create import CreateCommand
from server.service.error.back_error import BackError
from server.service.slack.message import MessageStatus, MessageVisibility
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "42"
team_id = "1337"
user_id = "4321"


@pytest.mark.parametrize(
    "text, expected_message",
    [
        (
            "test_create --label my label --pick-list 1 2 3 --self-exclude",
            "Command test_create successfully created.",
        ),
        (
            "test_create -l my label -p 1 2 3 -s",
            "Command test_create successfully created.",
        ),
        (
            "test_create --label my label --pick-list 1 2 3 --self-exclude",
            "my label",
        ),
        (
            "test_create -l my label -p 1 2 3 -s",
            "my label",
        ),
        (
            "test_create --label my label --pick-list 1 2 3 --self-exclude",
            "['1', '2', '3']",
        ),
        (
            "test_create -l my label -p 1 2 3 -s",
            "['1', '2', '3']",
        ),
        (
            "test_create -l my label -p 1 2 3 -s",
            "User using the slash command excluded.",
        ),
        (
            "test_create --label my label --pick-list 1 2 3 --self-exclude",
            "User using the slash command excluded.",
        ),
        (
            "test_create --label my label --pick-list 1 2 3 --self-exclude True",  # noqa E501
            "User using the slash command excluded.",
        ),
        (
            "test_create --label my label --pick-list 1 2 3 --self-exclude False",  # noqa E501
            "User using the slash command not excluded.",
        ),
        (
            "test_create --label my label --pick-list 1 2 3",
            "User using the slash command not excluded.",
        ),
        (
            "test_create --label my label --pick-list all_members",
            "['<@1234>', '<@2345>', '<@3456>']",
        ),
        (
            "test_create --label my label --pick-list 1 2 3 --only-active-users",
            "Only active users are selected when using the slash command.",
        ),
        (
            "test_create --label my label --pick-list 1 2 3 -o False",
            "All items are selected when using the slash command.",
        ),
    ],
)
def test_create(text, expected_message, client):
    message = CreateCommand(text=text, team_id=team_id, channel_id=channel_id).exec(
        user_id
    )
    assert expected_message in message.content
    assert message.status == MessageStatus.SUCCESS
    assert message.visibility == MessageVisibility.NORMAL


@pytest.mark.parametrize("text", ["-h", "--help", "whatever -h"])
def test_create_help(text, client):
    message = CreateCommand(text=text, team_id=team_id, channel_id=channel_id).exec(
        user_id
    )
    assert "Command to create new slash commands." in message.content
    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.HIDDEN


def test_create_fail_if_already_exist(client):
    text = "test_create --label my label --pick-list 1 2 3 --self-exclude"
    CreateCommand(text=text, team_id=team_id, channel_id=channel_id).exec(user_id)

    with pytest.raises(BackError, match="Command already exists."):
        CreateCommand(text=text, team_id=team_id, channel_id=channel_id).exec(user_id)

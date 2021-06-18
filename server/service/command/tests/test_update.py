import pytest

import server.service.slack.tests.monkey_patch_request as monkey_patch_request  # noqa: F401, E501
from server.orm.command import Command
from server.service.command.args import ArgError
from server.service.command.update import UpdateCommand
from server.service.slack.message import MessageStatus, MessageVisibility
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "1234"
user_id = "4321"
team_id = "1337"


@pytest.mark.parametrize(
    "text, expected_message",
    [
        (
            "test_update --label my new label",
            "Command test_update successfully updated.",
        ),
        (
            "test_update -l my new label",
            "Command test_update successfully updated.",
        ),
        (
            "test_update --label my new label",
            "my new label",
        ),
        (
            "test_update -l my new label",
            "my new label",
        ),
        (
            "test_update --pickList 1 2 3",
            "['1', '2', '3']",
        ),
        (
            "test_update -p 1 2 3",
            "['1', '2', '3']",
        ),
        (
            "test_update --pickList all_members",
            "['<@1234>', '<@2345>', '<@3456>']",
        ),
        (
            "test_update --addToPickList 3",
            "'3'",
        ),
        (
            "test_update -a 3",
            "'3'",
        ),
        (
            "test_update --removeFromPickList 1",
            "['2']",
        ),
        (
            "test_update -r 1",
            "['2']",
        ),
        (
            "test_update --label my new label",
            "User using the slash command excluded.",
        ),
        (
            "test_update --label my new label --selfExclude",
            "User using the slash command excluded.",
        ),
        (
            "test_update --label my new label --selfExclude True",
            "User using the slash command excluded.",
        ),
        (
            "test_update --label my new label --selfExclude False",
            "User using the slash command not excluded.",
        ),
    ],
)
def test_update(text, expected_message, client):
    Command.create("test_update", channel_id, "label", ["1", "2"], True, user_id)
    message = UpdateCommand(text=text, team_id=team_id, channel_id=channel_id).exec(
        user_id
    )
    assert expected_message in message.content
    assert message.status == MessageStatus.SUCCESS
    assert message.visibility == MessageVisibility.NORMAL


@pytest.mark.parametrize("text", ["-h", "--help", "whatever -h"])
def test_create_help(text, client):
    message = UpdateCommand(text=text, team_id=team_id, channel_id=channel_id).exec(
        user_id
    )
    assert "Update a given command." in message.content
    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.HIDDEN


def test_update_fail_if_command_does_not_exist(client):
    text = "test_update --label my label --pickList 1 2 3 --selfExclude"

    with pytest.raises(ArgError, match="Command test_update does not exist."):
        UpdateCommand(text=text, team_id=team_id, channel_id=channel_id).exec(user_id)

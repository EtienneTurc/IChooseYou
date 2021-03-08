import pytest

import server.slack.tests.monkey_patch_request as monkey_patch_request  # noqa: F401
from server.blueprint.back_error import BackError
from server.command.create import CreateCommand
from server.slack.message_status import MessageStatus, MessageVisibility
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "42"
user_id = "4321"


@pytest.mark.parametrize(
    "text, expected_message",
    [
        (
            "--commandName test_create --label my label --pickList 1 2 3 --selfExclude",
            "Command test_create successfully created.",
        ),
        (
            "--commandName test_create --label my label --pickList 1 2 3 --selfExclude",
            "my label",
        ),
        (
            "--commandName test_create --label my label --pickList 1 2 3 --selfExclude",
            "['1', '2', '3']",
        ),
        (
            "--commandName test_create --label my label --pickList 1 2 3 --selfExclude",
            "User using the slash command excluded.",
        ),
        (
            "--commandName test_create --label my label --pickList 1 2 3 --selfExclude True",  # noqa E501
            "User using the slash command excluded.",
        ),
        (
            "--commandName test_create --label my label --pickList 1 2 3 --selfExclude False",  # noqa E501
            "User using the slash command not excluded.",
        ),
        (
            "--commandName test_create --label my label --pickList 1 2 3",
            "User using the slash command not excluded.",
        ),
        (
            "--commandName test_create --label my label --pickList all_members",
            "['<@1234>', '<@2345>', '<@3456>']",
        ),
    ],
)
def test_create(text, expected_message, client):
    message, message_status, message_visibility = CreateCommand(text, channel_id).exec(
        user_id
    )
    assert expected_message in message
    assert message_status == MessageStatus.SUCCESS
    assert message_visibility == MessageVisibility.NORMAL


def test_create_fail_if_already_exist(client):
    text = "--commandName test_create --label my label --pickList 1 2 3 --selfExclude"
    CreateCommand(text, channel_id).exec(user_id)

    with pytest.raises(BackError, match="Command already exists."):
        CreateCommand(text, channel_id).exec(user_id)

import pytest

from server.blueprint.back_error import BackError
from server.command.create import CreateCommand
from server.slack.message_status import MessageStatus
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "42"


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
    ],
)
def test_create(text, expected_message, client):
    message, message_status = CreateCommand(text, channel_id).exec()
    assert expected_message in message
    assert message_status == MessageStatus.SUCCESS


def test_create_fail_if_already_exist(client):
    text = "--commandName test_create --label my label --pickList 1 2 3 --selfExclude"
    CreateCommand(text, channel_id).exec()

    with pytest.raises(BackError, match="Command already exists."):
        CreateCommand(text, channel_id).exec()

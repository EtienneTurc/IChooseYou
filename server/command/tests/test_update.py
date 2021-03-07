import pytest

from server.command.args import ArgError
from server.command.update import UpdateCommand
from server.orm.command import Command
from server.slack.message_status import MessageStatus
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "1234"
user_id = "4321"


@pytest.mark.parametrize(
    "text, expected_message",
    [
        (
            "--commandName test_update --label my new label",
            "Command test_update successfully updated.",
        ),
        (
            "--commandName test_update --label my new label",
            "my new label",
        ),
        (
            "--commandName test_update --pickList 1 2 3",
            "['1', '2', '3']",
        ),
        (
            "--commandName test_update --addToPickList 3",
            "'3'",
        ),
        (
            "--commandName test_update --removeFromPickList 1",
            "['2']",
        ),
        (
            "--commandName test_update --label my new label",
            "User using the slash command excluded.",
        ),
        (
            "--commandName test_update --label my new label --selfExclude",
            "User using the slash command excluded.",
        ),
        (
            "--commandName test_update --label my new label --selfExclude True",
            "User using the slash command excluded.",
        ),
        (
            "--commandName test_update --label my new label --selfExclude False",
            "User using the slash command not excluded.",
        ),
    ],
)
def test_update(text, expected_message, client):
    Command.create("test_update", channel_id, "label", ["1", "2"], True, user_id)
    message, message_status = UpdateCommand(text, channel_id).exec(user_id)
    assert expected_message in message
    assert message_status == MessageStatus.SUCCESS


def test_update_fail_if_command_does_not_exist(client):
    text = "--commandName test_update --label my label --pickList 1 2 3 --selfExclude"

    with pytest.raises(ArgError, match="Command test_update does not exist."):
        UpdateCommand(text, channel_id).exec(user_id)

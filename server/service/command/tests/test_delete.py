import pytest

from server.orm.command import Command
from server.service.command.args import ArgError
from server.service.command.delete import DeleteCommand
from server.service.slack.message import MessageStatus, MessageVisibility
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "1234"
team_id = "1337"


def test_delete(client):
    Command.create("test_delete", channel_id, "label", ["1", "2"], True, "4321")
    text = "test_delete"
    message = DeleteCommand(text=text, team_id=team_id, channel_id=channel_id).exec()
    assert "Command test_delete successfully deleted." == message.content
    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.NORMAL


@pytest.mark.parametrize("text", ["-h", "--help", "whatever -h"])
def test_delete_help(text, client):
    message = DeleteCommand(text=text, team_id=team_id, channel_id=channel_id).exec()
    assert "Delete a given command." in message.content
    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.HIDDEN


def test_delete_fail_if_command_does_not_exist(client):
    text = "test_delete"
    with pytest.raises(ArgError, match="Command test_delete does not exist."):
        DeleteCommand(text=text, team_id=team_id, channel_id=channel_id).exec()
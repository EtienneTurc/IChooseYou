import pytest

from server.command.args import ArgError
from server.command.delete import DeleteCommand
from server.orm.command import Command
from server.slack.message_status import MessageStatus, MessageVisibility
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "1234"


def test_delete(client):
    Command.create("test_delete", channel_id, "label", ["1", "2"], True, "4321")
    text = "test_delete"
    message, message_status, message_visibility = DeleteCommand(text, channel_id).exec()
    assert "Command test_delete successfully deleted." == message
    assert message_status == MessageStatus.INFO
    assert message_visibility == MessageVisibility.NORMAL


def test_delete_fail_if_command_does_not_exist(client):
    text = "test_delete"
    with pytest.raises(ArgError, match="Command test_delete does not exist."):
        DeleteCommand(text, channel_id).exec()

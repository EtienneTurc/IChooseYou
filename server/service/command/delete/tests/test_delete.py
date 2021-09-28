import pytest

from server.orm.command import Command
from server.service.command.args import ArgError
from server.service.slack.message import MessageStatus, MessageVisibility
from server.service.strategy.enum import Strategy
from server.tests.test_app import *  # noqa: F401, F403
from server.service.command.delete.processor import delete_command_processor
from server.service.slack.response.response_type import SlackResponseType

channel_id = "1234"
team_id = "1337"
command_name = "test_delete"


def test_delete(client):
    Command.create(
        name=command_name,
        channel_id=channel_id,
        label="label",
        pick_list=["1", "2"],
        weight_list=[1 / 2, 1 / 2],
        strategy=Strategy.uniform.name,
        self_exclude=True,
        only_active_users=False,
        created_by_user_id="4321",
    )
    response = delete_command_processor(
        channel_id=channel_id, command_to_delete=command_name
    )

    assert response.type == SlackResponseType.SLACK_SEND_MESSAGE_IN_CHANNEL.value

    message = response.data["message"]

    assert "Command test_delete successfully deleted." == message.content
    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.NORMAL


def test_delete_fail_if_command_does_not_exist(client):
    with pytest.raises(ArgError, match="Command test_delete does not exist."):
        delete_command_processor(channel_id=channel_id, command_to_delete=command_name)

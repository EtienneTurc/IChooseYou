import pytest

from server.orm.command import Command
from server.service.command.clean_deleted_users.processor import \
    clean_deleted_users_command_processor
from server.service.slack.message import MessageStatus, MessageVisibility
from server.service.strategy.enum import Strategy
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "42"
team_id = "1337"
user_id = "4321"

default_command = {
    "name": "command_name",
    "channel_id": channel_id,
    "label": "label",
    "description": "my super description",
    "self_exclude": True,
    "only_active_users": False,
    "strategy": Strategy.uniform.name,
    "created_by_user_id": user_id,
}


def test_clean_deleted_users_update_command(client):
    pick_list = ["<@1234>", "<@deleted>"]
    weight_list = [1 / 2, 1 / 2]
    command = Command.create(
        **default_command, pick_list=pick_list, weight_list=weight_list
    )

    response = clean_deleted_users_command_processor(
        user_id=user_id, team_id=team_id, channel_id=channel_id
    )

    message = response.get("message")

    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.NORMAL
    assert (
        message.content
        == f"{user_id} cleaned up the deleted users from the pick lists :broom:"
    )

    updated_command = Command.find_by_id(command._id)
    assert updated_command.pick_list == pick_list[:1]


def test_clean_deleted_users_delete_command(client):
    pick_list = ["<@deleted>"]
    weight_list = [1]
    command = Command.create(
        **default_command, pick_list=pick_list, weight_list=weight_list
    )

    response = clean_deleted_users_command_processor(
        user_id=user_id, team_id=team_id, channel_id=channel_id
    )

    message = response.get("message")

    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.NORMAL
    assert (
        message.content
        == f"{user_id} cleaned up the deleted users from the pick lists :broom:"
    )

    with pytest.raises(Command.DoesNotExist):
        Command.find_by_id(command._id)


def test_clean_deleted_users_nothing_to_do(client):
    pick_list = ["<@1234>", "<@2345>", "3"]
    weight_list = [1 / 3, 1 / 3, 1 / 3]
    command = Command.create(
        **default_command, pick_list=pick_list, weight_list=weight_list
    )

    response = clean_deleted_users_command_processor(
        user_id=user_id, team_id=team_id, channel_id=channel_id
    )

    message = response.get("message")

    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.HIDDEN
    assert (
        message.content == "No deleted users found. All pick commands are up to date."
    )

    not_updated_command = Command.find_by_id(command._id)
    assert not_updated_command.pick_list == pick_list

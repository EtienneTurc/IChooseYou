import pytest

import server.service.slack.tests.monkey_patch as monkey_patch_request  # noqa: F401, E501
from server.orm.command import Command
from server.service.command.update.processor import update_command_processor
from server.service.slack.message import MessageStatus, MessageVisibility
from server.service.strategy.enum import Strategy
from server.tests.test_app import *  # noqa: F401, F403
from marshmallow import ValidationError
from server.service.error.type.missing_element_error import MissingElementError

channel_id = "42"
team_id = "1337"
user_id = "4321"
command_name = "test_update"
default_pick_list = ["1", "2", "3"]

default_expected_command = {
    "name": command_name,
    "channel_id": channel_id,
    "label": "label",
    "description": "my super description",
    "pick_list": default_pick_list,
    "self_exclude": True,
    "only_active_users": False,
    "weight_list": [1 / 3, 1 / 3, 1 / 3],
    "strategy": Strategy.uniform.name,
    "created_by_user_id": user_id,
}


@pytest.mark.parametrize(
    "input_data, expected_command, expected_message",
    [
        (
            {},
            default_expected_command,
            "Command test_update successfully updated.",
        ),
        (
            {"label": "my new label"},
            {**default_expected_command, "label": "my new label"},
            "my new label",
        ),
        (
            {"description": "my new description"},
            {**default_expected_command, "description": "my new description"},
            "my new description",
        ),
        (
            {"pick_list": ["1", "2"]},
            {
                **default_expected_command,
                "pick_list": ["1", "2"],
                "weight_list": [1 / 2, 1 / 2],
            },
            "['1', '2']",
        ),
        # (
        #     {"pick_list": [PickListSpecialArg.ALL_MEMBERS.value]},
        #     {
        #         **default_expected_command,
        #         "pick_list": ["<@1234>", "<@2345>", "<@3456>"],
        #     },
        #     "['<@1234>', '<@2345>', '<@3456>']",
        # ),
        (
            {"add_to_pick_list": ["4"]},
            {
                **default_expected_command,
                "pick_list": ["1", "2", "3", "4"],
                "weight_list": [1 / 4, 1 / 4, 1 / 4, 1 / 4],
            },
            "['1', '2', '3', '4']",
        ),
        (
            {"remove_from_pick_list": ["2"]},
            {
                **default_expected_command,
                "pick_list": ["1", "3"],
                "weight_list": [1 / 2, 1 / 2],
            },
            "['1', '3']",
        ),
        (
            {},
            default_expected_command,
            "User using the slash command excluded.",
        ),
        (
            {"self_exclude": True},
            {**default_expected_command, "self_exclude": True},
            "User using the slash command excluded.",
        ),
        (
            {"self_exclude": False},
            {**default_expected_command, "self_exclude": False},
            "User using the slash command not excluded.",
        ),
        (
            {},
            default_expected_command,
            "All items are selected when using the slash command.",
        ),
        (
            {"only_active_users": True},
            {**default_expected_command, "only_active_users": True},
            "Only active users are selected when using the slash command.",
        ),
        (
            {"only_active_users": False},
            {**default_expected_command, "only_active_users": False},
            "All items are selected when using the slash command.",
        ),
        (
            {"strategy": Strategy.uniform.name},
            {**default_expected_command, "strategy": Strategy.uniform.name},
            "Strategy: uniform.",
        ),
        (
            {"strategy": Strategy.smooth.name},
            {**default_expected_command, "strategy": Strategy.smooth.name},
            "Strategy: smooth.",
        ),
        (
            {"strategy": Strategy.round_robin.name},
            {
                **default_expected_command,
                "strategy": Strategy.round_robin.name,
                "weight_list": [1, 0, 0],
            },
            "Strategy: round_robin.",
        ),
    ],
)
def test_update(input_data, expected_command, expected_message, client):
    Command.create(**default_expected_command)
    response = update_command_processor(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        command_to_update=command_name,
        **input_data,
    )

    message = response.get("message")

    assert expected_message in message.content
    assert message.status == MessageStatus.SUCCESS
    assert message.visibility == MessageVisibility.NORMAL

    updated_command = (
        Command.find_one_by_name_and_chanel(name=command_name, channel_id=channel_id)
        .to_son()
        .to_dict()
    )

    for key in expected_command:
        assert updated_command[key] == expected_command[key]


def test_update_fail_if_command_does_not_exist(client):
    with pytest.raises(
        MissingElementError, match="Command test_update does not exist."
    ):
        update_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            command_to_update=command_name,
        )


def test_create_fail_if_command_name_empty(client):
    error_message = "Field may not be empty."
    with pytest.raises(ValidationError, match=error_message):
        update_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            command_to_update="",
        )


def test_create_fail_if_pick_list_is_None(client):
    error_message = "Field may not be null."
    with pytest.raises(ValidationError, match=error_message):
        update_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            command_to_update=command_name,
            pick_list=None,
        )


def test_create_fail_if_pick_list_empty(client):
    error_message = "Field may not be empty."
    with pytest.raises(ValidationError, match=error_message):
        update_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            command_to_update=command_name,
            pick_list=[],
        )


def test_create_fail_if_non_valid_strategy(client):
    error_message = "boop is not a valid strategy."
    with pytest.raises(ValidationError, match=error_message):
        update_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            new_command_name=command_name,
            strategy="boop",
            pick_list=default_pick_list,
        )

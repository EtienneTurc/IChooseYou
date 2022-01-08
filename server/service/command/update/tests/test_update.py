import pytest
from marshmallow import ValidationError

import server.service.slack.tests.monkey_patch as monkey_patch_request  # noqa: F401, E501
from server.orm.command import Command
from server.service.command.update.processor import update_command_processor
from server.service.error.type.missing_element_error import MissingElementError
from server.service.slack.message import MessageStatus, MessageVisibility
from server.service.strategy.enum import Strategy
from server.tests.test_app import *  # noqa: F401, F403

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
    "input_data, expected_command, expected_message, non_expected_message",
    [
        (
            {},
            default_expected_command,
            f"{user_id} updated *{command_name}*.",
            None,
        ),
        (
            {"label": "my new label"},
            {**default_expected_command, "label": "my new label"},
            "Command message changed to: Hey ! <@user> choose <selected_item> my new label",  # noqa E501
            None,
        ),
        (
            {"description": "my new description"},
            {**default_expected_command, "description": "my new description"},
            None,
            "my new description",
        ),
        (
            {"pick_list": ["1", "2"]},
            {
                **default_expected_command,
                "pick_list": ["1", "2"],
                "weight_list": [1 / 2, 1 / 2],
            },
            "Users removed: 3.",
            None,
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
            "New users added: 4.",
            None,
        ),
        (
            {"remove_from_pick_list": ["2"]},
            {
                **default_expected_command,
                "pick_list": ["1", "3"],
                "weight_list": [1 / 2, 1 / 2],
            },
            "Users removed: 2.",
            None,
        ),
        (
            {"remove_from_pick_list": ["2", "3"]},
            {
                **default_expected_command,
                "pick_list": ["1"],
                "weight_list": [1],
            },
            "Users removed: 2 and 3.",
            None,
        ),
        (
            {"self_exclude": True},
            {**default_expected_command, "self_exclude": True},
            None,
            "User running the command is now",
        ),
        (
            {"self_exclude": False},
            {**default_expected_command, "self_exclude": False},
            "User running the command is now included in the pick.",
            None,
        ),
        (
            {"only_active_users": True},
            {**default_expected_command, "only_active_users": True},
            "Only active users are now picked",
            None,
        ),
        (
            {"only_active_users": False},
            {**default_expected_command, "only_active_users": False},
            None,
            "active",
        ),
        (
            {"strategy": Strategy.uniform.name},
            {**default_expected_command, "strategy": Strategy.uniform.name},
            None,
            "Strategy changed to",
        ),
        (
            {"strategy": Strategy.smooth.name},
            {**default_expected_command, "strategy": Strategy.smooth.name},
            "Strategy changed to smooth.",
            None,
        ),
        (
            {"strategy": Strategy.round_robin.name},
            {
                **default_expected_command,
                "strategy": Strategy.round_robin.name,
                "weight_list": [1, 0, 0],
            },
            "Strategy changed to round_robin.",
            None,
        ),
    ],
)
def test_update(
    input_data, expected_command, expected_message, non_expected_message, client
):
    Command.create(**default_expected_command)
    response = update_command_processor(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        command_to_update=command_name,
        **input_data,
    )

    message = response.get("message")

    if expected_message:
        assert expected_message in message.content
    if non_expected_message:
        assert non_expected_message not in message.content
    assert message.status == MessageStatus.INFO
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

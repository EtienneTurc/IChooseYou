import pytest
from marshmallow import ValidationError

import server.service.slack.tests.monkey_patch as monkey_patch_request  # noqa: F401, E501
from server.blueprint.slash_command.action import KNOWN_SLASH_COMMANDS_ACTIONS
from server.orm.command import Command
from server.service.command.create.processor import create_command_processor
from server.service.command.enum import PickListSpecialArg
from server.service.error.type.bad_request_error import BadRequestError
from server.service.slack.message import MessageStatus, MessageVisibility
from server.service.strategy.enum import Strategy
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "42"
team_id = "1337"
user_id = "4321"
command_name = "test_create"
default_pick_list = ["1", "2", "3"]


default_expected_command = {
    "name": command_name,
    "channel_id": channel_id,
    "label": "",
    "description": "",
    "pick_list": default_pick_list,
    "self_exclude": False,
    "only_active_users": False,
    "weight_list": [1 / 3, 1 / 3, 1 / 3],
    "strategy": Strategy.uniform.name,
    "created_by_user_id": user_id,
}


@pytest.mark.parametrize(
    "input_data, expected_command, expected_message",
    [
        (
            {"label": "my label"},
            {**default_expected_command, "label": "my label"},
            f"{user_id} created *{command_name}*.",
        ),
        (
            {"description": "my super awesome description"},
            {**default_expected_command, "description": "my super awesome description"},
            "my super awesome description",
        ),
        (
            {"pick_list": ["1", "2"]},
            {
                **default_expected_command,
                "pick_list": ["1", "2"],
                "weight_list": [1 / 2, 1 / 2],
            },
            "\nItems in the pick list are: 1 and 2.",
        ),
        (
            {"pick_list": [PickListSpecialArg.ALL_MEMBERS.value]},
            {
                **default_expected_command,
                "pick_list": ["<@1234>", "<@2345>", "<@3456>"],
            },
            "\nItems in the pick list are: <@1234>, <@2345> and <@3456>.",
        ),
        (
            {"self_exclude": True},
            {**default_expected_command, "self_exclude": True},
            None,
        ),
        (
            {"only_active_users": True},
            {**default_expected_command, "only_active_users": True},
            None,
        ),
        (
            {"only_active_users": False},
            {**default_expected_command, "only_active_users": False},
            None,
        ),
        (
            {"strategy": Strategy.uniform.name},
            {**default_expected_command, "strategy": Strategy.uniform.name},
            None,
        ),
        (
            {"strategy": Strategy.smooth.name},
            {**default_expected_command, "strategy": Strategy.smooth.name},
            None,
        ),
        (
            {"strategy": Strategy.round_robin.name},
            {
                **default_expected_command,
                "strategy": Strategy.round_robin.name,
                "weight_list": [1, 0, 0],
            },
            None,
        ),
    ],
)
def test_create(input_data, expected_command, expected_message, client):
    if not input_data.get("pick_list"):
        input_data["pick_list"] = default_pick_list

    response = create_command_processor(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        new_command_name=command_name,
        **input_data,
    )

    message = response.get("message")
    if expected_message:
        assert expected_message in message.content
    assert message.status == MessageStatus.SUCCESS
    assert message.visibility == MessageVisibility.NORMAL

    created_command = (
        Command.find_one_by_name_and_chanel(name=command_name, channel_id=channel_id)
        .to_son()
        .to_dict()
    )

    for key in expected_command:
        assert created_command[key] == expected_command[key]


def test_create_fail_if_already_exist(client):
    create_command_processor(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        new_command_name=command_name,
        pick_list=["1", "2", "3"],
    )

    with pytest.raises(
        BadRequestError, match=f"Command {command_name} already exists."
    ):
        create_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            new_command_name=command_name,
            pick_list=["1", "2", "3"],
        )


def test_create_fail_if_command_name_empty(client):
    error_message = "Field may not be empty."
    with pytest.raises(ValidationError, match=error_message):
        create_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            new_command_name="",
            pick_list=default_pick_list,
        )


def test_create_fail_if_command_name_in_multiple_words(client):
    error_message = "Command name must be a single word, i.e without spaces."
    with pytest.raises(ValidationError, match=error_message):
        create_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            new_command_name="a command",
            pick_list=default_pick_list,
        )


@pytest.mark.parametrize("new_command_name", KNOWN_SLASH_COMMANDS_ACTIONS)
def test_create_fail_if_command_name_is_a_keyword(new_command_name, client):
    error_message = "Command name can not be one of these: create, update, delete, randomness, instant and clean_deleted_users."  # noqa E501
    with pytest.raises(ValidationError, match=error_message):
        create_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            new_command_name=new_command_name,
        )


def test_create_fail_if_pick_list_is_None(client):
    error_message = "Field may not be null."
    with pytest.raises(ValidationError, match=error_message):
        create_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            new_command_name=command_name,
            pick_list=None,
        )


def test_create_fail_if_pick_list_empty(client):
    error_message = "Field may not be empty."
    with pytest.raises(ValidationError, match=error_message):
        create_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            new_command_name=command_name,
            pick_list=[],
        )


def test_create_fail_if_non_valid_strategy(client):
    error_message = "boop is not a valid strategy."
    with pytest.raises(ValidationError, match=error_message):
        create_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            new_command_name=command_name,
            strategy="boop",
            pick_list=default_pick_list,
        )

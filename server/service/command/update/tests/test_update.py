import pytest
from marshmallow import ValidationError

from server.blueprint.slash_command.action import KNOWN_SLASH_COMMANDS_ACTIONS
from server.orm.command import Command
from server.service.command.update.processor import update_command_processor
from server.service.error.type.missing_element_error import MissingElementError
from server.service.slack.message import MessageStatus, MessageVisibility
from server.service.slack.tests.monkey_patch import *  # noqa: F401, F403
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
    "weight_list": [1 / 4, 1 / 4, 2 / 4],
    "strategy": Strategy.smooth.name,
    "created_by_user_id": user_id,
}


@pytest.mark.parametrize(
    "input_data, expected_command, expected_message, non_expected_message",
    [
        (
            {"label": "my new label"},
            {**default_expected_command, "label": "my new label"},
            "Command message changed to: Hey ! <@user> choose <selected_item> my new label",  # noqa E501
            None,
        ),
        (
            {"label": ""},
            {**default_expected_command, "label": ""},
            "Command message changed to: Hey ! <@user> choose <selected_item>",  # noqa E501
            None,
        ),
        (
            {"description": "my new description"},
            {**default_expected_command, "description": "my new description"},
            "my new description",
            None,
        ),
        (
            {"description": ""},
            {**default_expected_command, "description": ""},
            "Command description removed.",
            None,
        ),
        (
            {"pick_list": ["1", "2"]},
            {
                **default_expected_command,
                "pick_list": ["1", "2"],
                "weight_list": [1 / 2, 1 / 2],
            },
            "Items removed: 3.",
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
                "weight_list": [3 / 16, 3 / 16, 6 / 16, 4 / 16],
            },
            "New items added: 4.",
            None,
        ),
        (
            {"remove_from_pick_list": ["2"]},
            {
                **default_expected_command,
                "pick_list": ["1", "3"],
                "weight_list": [1 / 3, 2 / 3],
            },
            "Items removed: 2.",
            None,
        ),
        (
            {"remove_from_pick_list": ["2", "3"]},
            {
                **default_expected_command,
                "pick_list": ["1"],
                "weight_list": [1],
            },
            "Items removed: 2 and 3.",
            None,
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
            {"strategy": Strategy.uniform.name},
            {
                **default_expected_command,
                "strategy": Strategy.uniform.name,
                "weight_list": [1 / 3, 1 / 3, 1 / 3],
            },
            "Strategy changed to uniform.",
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


@pytest.mark.parametrize(
    "input_data",
    [
        {},
        {"label": default_expected_command["label"]},
        {"description": default_expected_command["description"]},
        {"pick_list": default_expected_command["pick_list"]},
        {"add_to_pick_list": []},
        {"remove_from_pick_list": []},
        {"self_exclude": default_expected_command["self_exclude"]},
        {"only_active_users": default_expected_command["only_active_users"]},
        {"strategy": default_expected_command["strategy"]},
    ],
)
def test_update_without_changes(input_data, client):
    Command.create(**default_expected_command)
    response = update_command_processor(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        command_to_update=command_name,
        **input_data,
    )

    message = response.get("message")

    assert f"Nothing to update for command *{command_name}*." in message.content
    assert message.status == MessageStatus.ERROR
    assert message.visibility == MessageVisibility.HIDDEN


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


def test_update_fail_if_command_name_empty(client):
    error_message = "Field may not be empty."
    with pytest.raises(ValidationError, match=error_message):
        update_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            command_to_update="",
        )


@pytest.mark.parametrize("new_command_name", KNOWN_SLASH_COMMANDS_ACTIONS)
def test_update_fail_if_command_name_is_a_keyword(new_command_name, client):
    error_message = "Command name can not be one of these: create, update, delete, randomness, instant and clean_deleted_users."  # noqa E501
    with pytest.raises(ValidationError, match=error_message):
        update_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            command_to_update=command_name,
            new_command_name=new_command_name,
        )


def test_update_fail_if_pick_list_is_None(client):
    error_message = "Field may not be null."
    with pytest.raises(ValidationError, match=error_message):
        update_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            command_to_update=command_name,
            pick_list=None,
        )


def test_update_fail_if_pick_list_empty(client):
    error_message = "Field may not be empty."
    with pytest.raises(ValidationError, match=error_message):
        update_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            command_to_update=command_name,
            pick_list=[],
        )


def test_update_fail_if_non_valid_strategy(client):
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

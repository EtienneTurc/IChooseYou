import pytest

import server.service.slack.tests.monkey_patch as monkey_patch_request  # noqa: F401, E501
from server.service.error.back_error import BackError
from server.service.slack.message import MessageStatus, MessageVisibility
from server.tests.test_app import *  # noqa: F401, F403
from server.service.command.create.processor import create_command_processor
from server.service.strategy.enum import Strategy
from server.service.command.enum import PickListSpecialArg
from server.orm.command import Command
from server.service.slack.response.response_type import SlackResponseType


channel_id = "42"
team_id = "1337"
user_id = "4321"
command_name = "test_create"
default_pick_list = [1, 2, 3]


default_expected_command = {
    "name": command_name,
    "channel_id": channel_id,
    "label": "",
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
            "Command test_create successfully created.",
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
        (
            {"pick_list": [PickListSpecialArg.ALL_MEMBERS.value]},
            {
                **default_expected_command,
                "pick_list": ["<@1234>", "<@2345>", "<@3456>"],
            },
            "['<@1234>', '<@2345>', '<@3456>']",
        ),
        (
            {"self_exclude": True},
            {**default_expected_command, "self_exclude": True},
            "User using the slash command excluded.",
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

    assert response.type == SlackResponseType.SLACK_SEND_MESSAGE_IN_CHANNEL.value

    message = response.data["message"]
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
        pick_list=[1, 2, 3],
    )

    with pytest.raises(BackError, match="Command already exists."):
        create_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            new_command_name=command_name,
            pick_list=[1, 2, 3],
        )


# TODO with schema validation
# def test_create_fail_if_pick_list_empty(client):
#     with pytest.raises(ArgError):
#         create_command_processor(
#             user_id=user_id,
#             team_id=team_id,
#             channel_id=channel_id,
#             new_command_name=command_name,
#             pick_list=[],
#         )

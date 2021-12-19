import pytest
from marshmallow import ValidationError

import server.service.slack.tests.monkey_patch as monkey_patch_request  # noqa: F401, E501
from server.service.command.instant.processor import instant_command_processor
from server.service.error.type.bad_request_error import BadRequestError
from server.service.error.type.missing_element_error import MissingElementError
from server.service.slack.message import MessageVisibility
from server.tests.test_fixture import *  # noqa: F401, F403

user_id = "1234"
team_id = "1234"
channel_id = "1234"
label = "my instant command"
pick_list = ["1", "2"]
number_of_items_to_select = 1
self_exclude = False
only_active_users = False


def test_instant_command():
    response = instant_command_processor(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        label=label,
        pick_list=pick_list,
        number_of_items_to_select=number_of_items_to_select,
        self_exclude=self_exclude,
        only_active_users=only_active_users,
    )

    message = response.get("message")
    selected_items = response.get("selected_items")
    assert selected_items == ["1"] or ["2"]

    assert f"Hey ! <@{user_id}> choose {selected_items[0]}" in message.content
    assert label in message.content

    assert message.visibility == MessageVisibility.NORMAL
    assert message.as_attachment is False


def test_custom_command_self_exclude():
    response = instant_command_processor(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        label=label,
        pick_list=[user_id, "2"],
        number_of_items_to_select=number_of_items_to_select,
        self_exclude=True,
        only_active_users=only_active_users,
    )

    message = response.get("message")
    assert "choose 2" in message.content

    selected_items = response.get("selected_items")
    assert selected_items == ["2"]


def test_custom_command_self_exclude_error():
    error_message = "Pick list contains only the user using the command.*selfExclude.*True.*"  # noqa E501
    with pytest.raises(BadRequestError, match=error_message):
        instant_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            label=label,
            pick_list=[user_id],
            number_of_items_to_select=number_of_items_to_select,
            self_exclude=True,
            only_active_users=only_active_users,
        )


def test_custom_command_only_active_users():
    response = instant_command_processor(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        label=label,
        pick_list=[f"<@{user_id}|name>", "<@4321|name>"],
        number_of_items_to_select=number_of_items_to_select,
        self_exclude=self_exclude,
        only_active_users=True,
    )

    message = response.get("message")
    assert f"<@{user_id}|name>" in message.content

    selected_items = response.get("selected_items")
    assert selected_items == [f"<@{user_id}|name>"]


def test_custom_only_active_users_error():
    error_message = "No active users to select found."
    with pytest.raises(MissingElementError, match=error_message):
        instant_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            label=label,
            pick_list=["<@4321|name>"],
            number_of_items_to_select=number_of_items_to_select,
            self_exclude=self_exclude,
            only_active_users=True,
        )


@pytest.mark.parametrize(
    "number_of_items_to_select, expected_message, expected_items",
    [
        (1, "choose 1", ["1"]),
        (2, "choose 1 and 3", ["1", "3"]),
        (3, "choose 1, 3 and 2", ["1", "3", "2"]),
    ],
)
def test_custom_command_multi_select(
    number_of_items_to_select,
    expected_message,
    expected_items,
    set_seed,
):
    response = instant_command_processor(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        label=label,
        pick_list=["1", "2", "3"],
        number_of_items_to_select=number_of_items_to_select,
        self_exclude=self_exclude,
        only_active_users=only_active_users,
    )

    message = response.get("message")
    assert expected_message in message.content

    selected_items = response.get("selected_items")
    assert selected_items == expected_items


def test_create_fail_if_number_of_items_to_select_is_0():
    error_message = "Field may be greater or equal to 1."
    with pytest.raises(ValidationError, match=error_message):
        instant_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id=channel_id,
            label=label,
            pick_list=["1", "2", "3"],
            number_of_items_to_select=0,
            self_exclude=self_exclude,
            only_active_users=only_active_users,
        )

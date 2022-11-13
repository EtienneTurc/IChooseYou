import pytest
from marshmallow import ValidationError

from server.orm.command import Command
from server.service.command.custom.processor import custom_command_processor
from server.service.command.custom.tests.command_fixture import *  # noqa: F401, F403
from server.service.error.type.missing_element_error import MissingElementError
from server.service.slack.message import MessageVisibility
from server.service.wheel.constant import (LEGEND_WIDTH, NB_FRAMES, WHEEL_HEIGHT,
                                           WHEEL_WIDTH)
from server.tests.test_fixture import *  # noqa: F401, F403

user_id = "1234"
team_id = "1234"


def test_custom_command(basic_command):
    response = custom_command_processor(
        command_name=basic_command.name,
        additional_text="",
        number_of_items_to_select=1,
        channel_id=basic_command.channel_id,
        team_id=team_id,
        user_id=user_id,
    )

    message = response.get("message")
    assert f"Hey ! <@{user_id}> choose " in message.content
    assert basic_command.label in message.content

    assert message.visibility == MessageVisibility.NORMAL
    assert message.as_attachment is False


def test_custom_command_self_exclude(command_for_self_exclude):
    response = custom_command_processor(
        command_name=command_for_self_exclude.name,
        additional_text="",
        number_of_items_to_select=1,
        channel_id=command_for_self_exclude.channel_id,
        team_id=team_id,
        user_id=user_id,
    )

    message = response.get("message")
    assert "choose 2" in message.content

    selected_items = response.get("selected_items")
    assert selected_items == ["2"]


def test_custom_command_self_exclude_error(command_for_self_exclude_error):
    error_message = "Pick list contains only the user using the command."  # noqa E501
    with pytest.raises(MissingElementError, match=error_message):
        custom_command_processor(
            command_name=command_for_self_exclude_error.name,
            additional_text="",
            number_of_items_to_select=1,
            channel_id=command_for_self_exclude_error.channel_id,
            team_id=team_id,
            user_id=user_id,
        )


def test_custom_command_only_active_users(command_for_active_users):
    response = custom_command_processor(
        command_name=command_for_active_users.name,
        additional_text="",
        number_of_items_to_select=1,
        channel_id=command_for_active_users.channel_id,
        team_id=team_id,
        user_id=user_id,
    )

    message = response.get("message")
    assert f"<@{user_id}|name>" in message.content

    selected_items = response.get("selected_items")
    assert selected_items == [f"<@{user_id}|name>"]


def test_custom_only_active_users_error(command_with_no_active_users):
    error_message = "All users in the pick list are inactive."
    with pytest.raises(MissingElementError, match=error_message):
        custom_command_processor(
            command_name=command_with_no_active_users.name,
            additional_text="",
            number_of_items_to_select=1,
            channel_id=command_with_no_active_users.channel_id,
            team_id=team_id,
            user_id=user_id,
        )


@pytest.mark.parametrize(
    "additional_text, number_of_items_to_select, expected_message, expected_items",
    [
        ("", 1, "choose 2", ["2"]),
        ("", 2, "choose 2 and 3", ["2", "3"]),
        ("", 3, "choose 2, 3 and 1", ["2", "3", "1"]),
        (
            "custom text",
            2,
            "choose 2 and 3 basic command label custom text",
            ["2", "3"],
        ),
    ],
)
def test_custom_command_multi_select(
    additional_text,
    number_of_items_to_select,
    expected_message,
    expected_items,
    basic_command,
    set_seed,
):
    response = custom_command_processor(
        command_name=basic_command.name,
        additional_text=additional_text,
        number_of_items_to_select=number_of_items_to_select,
        channel_id=basic_command.channel_id,
        team_id=team_id,
        user_id=user_id,
    )

    message = response.get("message")
    assert expected_message in message.content

    selected_items = response.get("selected_items")
    assert selected_items == expected_items


@pytest.mark.parametrize(
    "number_of_items_to_select, expected_message, expected_items",
    [
        (1, "choose 2", ["2"]),
        (2, "choose 2 and 2", ["2", "2"]),
        (3, "choose 2, 2 and 1", ["2", "2", "1"]),
    ],
)
def test_custom_command_multi_select_with_duplicates_in_pick_list(
    number_of_items_to_select,
    expected_message,
    expected_items,
    command_with_duplicates_in_pick_list,
    set_seed,
):
    response = custom_command_processor(
        command_name=command_with_duplicates_in_pick_list.name,
        additional_text="",
        number_of_items_to_select=number_of_items_to_select,
        channel_id=command_with_duplicates_in_pick_list.channel_id,
        team_id=team_id,
        user_id=user_id,
    )

    message = response.get("message")
    assert expected_message in message.content

    selected_items = response.get("selected_items")
    assert selected_items == expected_items


def test_custom_command_updates_round_robin_command(
    command_with_round_robin_strategy,
    set_seed,
):
    response = custom_command_processor(
        command_name=command_with_round_robin_strategy.name,
        additional_text="",
        number_of_items_to_select=1,
        channel_id=command_with_round_robin_strategy.channel_id,
        team_id=team_id,
        user_id=user_id,
        should_update_command=True,
    )

    selected_items = response.get("selected_items")
    assert selected_items == ["2"]

    updated_command = Command.find_by_id(command_with_round_robin_strategy._id)
    assert updated_command.pick_list == ["2", "3", "1"]
    assert updated_command.weight_list == [0, 1, 0]


def test_create_fail_if_command_name_empty(client):
    error_message = "Field may not be empty."
    with pytest.raises(ValidationError, match=error_message):
        custom_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id="1",
            command_name="",
        )


def test_create_fail_if_number_of_items_to_select_is_0(client):
    error_message = "Must select at least 1 item."
    with pytest.raises(ValidationError, match=error_message):
        custom_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id="1",
            command_name="sqd",
            number_of_items_to_select=0,
        )


def test_create_fail_if_number_of_items_to_select_is_too_high(client):
    error_message = "Selecting more than 50 at once is prohibited."
    with pytest.raises(ValidationError, match=error_message):
        custom_command_processor(
            user_id=user_id,
            team_id=team_id,
            channel_id="1",
            command_name="sqd",
            number_of_items_to_select=51,
        )


def test_custom_command_with_no_wheel(basic_command):
    response = custom_command_processor(
        command_name=basic_command.name,
        additional_text="",
        number_of_items_to_select=1,
        channel_id=basic_command.channel_id,
        team_id=team_id,
        user_id=user_id,
        with_wheel=False,
    )

    with_wheel = response.get("with_wheel")
    assert with_wheel is False

    gif_frames = response.get("gif_frames")
    assert gif_frames is None


def test_custom_command_with_wheel(basic_command):
    response = custom_command_processor(
        command_name=basic_command.name,
        additional_text="",
        number_of_items_to_select=1,
        channel_id=basic_command.channel_id,
        team_id=team_id,
        user_id=user_id,
        with_wheel=True,
    )

    with_wheel = response.get("with_wheel")
    assert with_wheel is True

    gif_frames = response.get("gif_frames")
    assert gif_frames.shape == (NB_FRAMES, WHEEL_HEIGHT, WHEEL_WIDTH + LEGEND_WIDTH, 3)

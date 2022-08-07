import json

import pytest

import server.service.slack.tests.monkey_patch as monkey_patch  # noqa: F401
from server.blueprint.event.tests.conftest import *  # noqa: F401, F403
from server.blueprint.interactivity.action import BlueprintInteractivityBlockAction
from server.blueprint.interactivity.tests.helper import call_webhook
from server.service.slack.modal.instant_command_modal import (
    SlackInstantCommandModalActionId, SlackInstantCommandModalBlockId)
from server.service.slack.modal.upsert_command_modal import (
    SlackUpsertCommandModalActionId, SlackUpsertCommandModalBlockId)
from server.tests.test_app import *  # noqa: F401, F403


def get_action_id_enum(instant_command_modal: bool):
    if instant_command_modal:
        return SlackInstantCommandModalActionId
    return SlackUpsertCommandModalActionId


def get_block_id_enum(instant_command_modal: bool):
    if instant_command_modal:
        return SlackInstantCommandModalBlockId
    return SlackUpsertCommandModalBlockId


SlackUpsertCommandModalBlockId.CHANNEL_BLOCK_ID

channel_id = "1234"


def build_default_view_values(
    instant_command_modal: bool,
    *,
    free_pick_list_item: str = None,
    user_pick_list_item: str = None,
):
    action_id_enum = get_action_id_enum(instant_command_modal)
    block_id_enum = get_block_id_enum(instant_command_modal)

    return {
        block_id_enum.CHANNEL_BLOCK_ID.value: {
            action_id_enum.CHANNEL_SELECT.value: {
                "selected_channel": channel_id,
            }
        },
        block_id_enum.FREE_PICK_LIST_BLOCK_ID.value: {
            action_id_enum.FREE_PICK_LIST_INPUT.value: {
                "type": "plain_text_input",
                "value": free_pick_list_item,
            }
        },
        block_id_enum.USER_PICK_LIST_BLOCK_ID.value: {
            action_id_enum.USER_PICK_LIST_INPUT.value: {
                "type": "users_select",
                "selected_user": user_pick_list_item,
            }
        },
    }


@pytest.mark.parametrize(
    "instant_command_modal, user_select_enabled, expected_value",
    [
        (False, False, True),
        (False, True, False),
        (True, False, True),
        (True, True, False),
    ],
)
def test_interactivity_switch_pick_list(
    instant_command_modal: bool, user_select_enabled, expected_value, client
):
    action_id = (
        BlueprintInteractivityBlockAction.INSTANT_COMMAND_MODAL_SWITCH_PICK_LIST_INPUT.value  # noqa E501
        if instant_command_modal
        else BlueprintInteractivityBlockAction.UPSERT_MODAL_SWITCH_PICK_LIST_INPUT.value
    )
    response, slack_message = call_webhook(
        client,
        action_id=action_id,
        type="block_actions",
        view_state_inputs=build_default_view_values(instant_command_modal),
        view_metadata={
            "user_select_enabled": user_select_enabled,
            "channel_id": channel_id,
        },
    )
    print(slack_message)
    assert response.status_code == 200
    assert "'type': 'modal'" in slack_message
    assert (
        "'private_metadata': '"
        + json.dumps(
            {
                "channel_id": channel_id,
                **({"command_name": None} if not instant_command_modal else {}),
                "pick_list": None,
                "user_select_enabled": expected_value,
            }
        )
    ) in slack_message


@pytest.mark.parametrize(
    "instant_command_modal, pick_list, item_to_add, expected_pick_list",
    [
        (False, [], "An item", ["An item"]),
        (
            False,
            ["Pick list not empty"],
            "with a second item",
            ["Pick list not empty", "with a second item"],
        ),
        (True, [], "An item", ["An item"]),
        (
            True,
            ["Pick list not empty"],
            "with a second item",
            ["Pick list not empty", "with a second item"],
        ),
    ],
)
def test_interactivity_add_free_element_to_pick_list(
    instant_command_modal: bool, pick_list, item_to_add, expected_pick_list, client
):
    action_id = (
        BlueprintInteractivityBlockAction.INSTANT_COMMAND_MODAL_ADD_FREE_ELEMENT_TO_PICK_LIST.value  # noqa E501
        if instant_command_modal
        else BlueprintInteractivityBlockAction.UPSERT_MODAL_ADD_FREE_ELEMENT_TO_PICK_LIST.value  # noqa E501
    )
    response, slack_message = call_webhook(
        client,
        action_id=action_id,
        type="block_actions",
        view_state_inputs=build_default_view_values(
            instant_command_modal, free_pick_list_item=item_to_add
        ),
        view_metadata={
            "channel_id": channel_id,
            "pick_list": pick_list,
        },
    )
    assert response.status_code == 200
    assert "'type': 'modal'" in slack_message
    assert (
        "'private_metadata': '"
        + json.dumps(
            {
                "channel_id": channel_id,
                **({"command_name": None} if not instant_command_modal else {}),
                "pick_list": expected_pick_list,
                "user_select_enabled": None,
            }
        )
    ) in slack_message


@pytest.mark.parametrize(
    "instant_command_modal, pick_list, item_to_add, expected_pick_list",
    [
        (False, [], "U1234", ["<@U1234>"]),
        (
            False,
            ["<@U1234>"],
            "U5678",
            ["<@U1234>", "<@U5678>"],
        ),
        (True, [], "U1234", ["<@U1234>"]),
        (
            True,
            ["<@U1234>"],
            "U5678",
            ["<@U1234>", "<@U5678>"],
        ),
    ],
)
def test_interactivity_add_user_to_pick_list(
    instant_command_modal: bool, pick_list, item_to_add, expected_pick_list, client
):
    action_id = (
        BlueprintInteractivityBlockAction.INSTANT_COMMAND_MODAL_ADD_USER_TO_PICK_LIST.value  # noqa E501
        if instant_command_modal
        else BlueprintInteractivityBlockAction.UPSERT_MODAL_ADD_USER_TO_PICK_LIST.value  # noqa E501
    )
    response, slack_message = call_webhook(
        client,
        action_id=action_id,
        type="block_actions",
        view_state_inputs=build_default_view_values(
            instant_command_modal, user_pick_list_item=item_to_add
        ),
        view_metadata={
            "channel_id": channel_id,
            "pick_list": pick_list,
        },
    )
    assert response.status_code == 200
    assert "'type': 'modal'" in slack_message
    assert (
        "'private_metadata': '"
        + json.dumps(
            {
                "channel_id": channel_id,
                **({"command_name": None} if not instant_command_modal else {}),
                "pick_list": expected_pick_list,
                "user_select_enabled": None,
            }
        )
    ) in slack_message


@pytest.mark.parametrize(
    "instant_command_modal, pick_list, index_of_item_to_remove, expected_pick_list",
    [
        (False, ["<@U1234>"], 0, []),
        (
            False,
            ["Pick list not empty", "with a user", "<@U1234>"],
            1,
            ["Pick list not empty", "<@U1234>"],
        ),
        (True, ["<@U1234>"], 0, []),
        (
            True,
            ["Pick list not empty", "with a user", "<@U1234>"],
            1,
            ["Pick list not empty", "<@U1234>"],
        ),
    ],
)
def test_interactivity_remove_element_from_pick_list(
    instant_command_modal: bool,
    pick_list,
    index_of_item_to_remove,
    expected_pick_list,
    client,
):
    action_id = (
        BlueprintInteractivityBlockAction.INSTANT_COMMAND_MODAL_REMOVE_ELEMENT_FROM_PICK_LIST.value  # noqa E501
        if instant_command_modal
        else BlueprintInteractivityBlockAction.UPSERT_MODAL_REMOVE_ELEMENT_FROM_PICK_LIST.value  # noqa E501
    )
    block_id_enum = get_block_id_enum(instant_command_modal)
    response, slack_message = call_webhook(
        client,
        action_id=action_id,
        action_block_id=f"{block_id_enum.REMOVE_FROM_PICK_LIST_BLOCK_ID}_{index_of_item_to_remove}",  # noqa E501
        type="block_actions",
        view_state_inputs=build_default_view_values(instant_command_modal),
        view_metadata={
            "channel_id": channel_id,
            "pick_list": pick_list,
        },
    )
    assert response.status_code == 200
    assert "'type': 'modal'" in slack_message
    assert (
        "'private_metadata': '"
        + json.dumps(
            {
                "channel_id": channel_id,
                **({"command_name": None} if not instant_command_modal else {}),
                "pick_list": expected_pick_list,
                "user_select_enabled": None,
            }
        )
    ) in slack_message

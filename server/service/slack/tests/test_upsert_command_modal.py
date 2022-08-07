import json

import pytest

import server.service.slack.tests.monkey_patch as monkey_patch  # noqa: F401
from server.service.slack.modal.upsert_command_modal import (
    SlackUpsertCommandModalActionId, SlackUpsertCommandModalBlockId,
    build_upsert_command_modal)
from server.service.slack.tests.helper import assert_modal_has_expected_block
from server.service.strategy.enum import Strategy
from server.tests.helper import match_object

default_update_input_data = {
    "channel_id": "42",
    "previous_channel_id": "41",
    "command_name": "test_build_upsert_command_modal_blocks",
    "description": "my super description",
    "label": "label",
    "user_select_enabled": True,
    "pick_list": ["1", "2", "<@4321>"],
    "free_pick_list_item": "Yo",
    "strategy": Strategy.smooth.name,
    "self_exclude": True,
    "only_active_users": True,
}


@pytest.mark.parametrize(
    "upsert, input_data, expected_block",
    [
        (
            False,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.CHANNEL_BLOCK_ID.value,
                "type": "input",
                "element": {
                    "type": "channels_select",
                    "action_id": SlackUpsertCommandModalActionId.CHANNEL_SELECT.value,
                },
            },
        ),
        (
            True,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.CHANNEL_BLOCK_ID.value,
                "type": "input",
                "element": {
                    "type": "channels_select",
                    "action_id": SlackUpsertCommandModalActionId.CHANNEL_SELECT.value,
                    "initial_channel": default_update_input_data["channel_id"],
                },
            },
        ),
        (
            False,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.COMMAND_NAME_BLOCK_ID.value,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": SlackUpsertCommandModalActionId.COMMAND_NAME_INPUT.value,
                },
            },
        ),
        (
            True,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.COMMAND_NAME_BLOCK_ID.value,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "initial_value": default_update_input_data["command_name"],
                    "action_id": SlackUpsertCommandModalActionId.COMMAND_NAME_INPUT.value,
                },
            },
        ),
        (
            False,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.DESCRIPTION_BLOCK_ID.value,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": SlackUpsertCommandModalActionId.DESCRIPTION_INPUT.value,
                },
                "optional": True,
            },
        ),
        (
            True,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.DESCRIPTION_BLOCK_ID.value,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "initial_value": default_update_input_data["description"],
                    "action_id": SlackUpsertCommandModalActionId.DESCRIPTION_INPUT.value,
                },
                "optional": True,
            },
        ),
        (
            False,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.LABEL_BLOCK_ID.value,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": SlackUpsertCommandModalActionId.LABEL_INPUT.value,
                },
                "optional": True,
            },
        ),
        (
            True,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.LABEL_BLOCK_ID.value,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "initial_value": default_update_input_data["label"],
                    "action_id": SlackUpsertCommandModalActionId.LABEL_INPUT.value,
                },
                "optional": True,
            },
        ),
        (
            False,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.USER_PICK_LIST_BLOCK_ID.value,
                "type": "input",
                "dispatch_action": True,
                "element": {
                    "type": "users_select",
                    "action_id": SlackUpsertCommandModalActionId.USER_PICK_LIST_INPUT.value,  # noqa E501
                },
                "optional": False,
            },
        ),
        (
            True,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.USER_PICK_LIST_BLOCK_ID.value,
                "type": "input",
                "dispatch_action": True,
                "element": {
                    "type": "users_select",
                    "action_id": SlackUpsertCommandModalActionId.USER_PICK_LIST_INPUT.value,  # noqa E501
                },
                "optional": True,
            },
        ),
        (
            False,
            {"user_select_enabled": False},
            {
                "type": "input",
                "block_id": SlackUpsertCommandModalBlockId.FREE_PICK_LIST_BLOCK_ID.value,
                "element": {
                    "type": "plain_text_input",
                    "action_id": SlackUpsertCommandModalActionId.FREE_PICK_LIST_INPUT.value,  # noqa E501
                    "initial_value": default_update_input_data["free_pick_list_item"],
                },
                "dispatch_action": True,
                "optional": False,
            },
        ),
        (
            True,
            {"user_select_enabled": False},
            {
                "type": "input",
                "block_id": SlackUpsertCommandModalBlockId.FREE_PICK_LIST_BLOCK_ID.value,
                "element": {
                    "type": "plain_text_input",
                    "action_id": SlackUpsertCommandModalActionId.FREE_PICK_LIST_INPUT.value,  # noqa E501
                    "initial_value": default_update_input_data["free_pick_list_item"],
                },
                "dispatch_action": True,
                "optional": True,
            },
        ),
        (
            False,
            {},
            {
                "block_id": SlackUpsertCommandModalBlockId.USER_SELECT_ENABLED_BLOCK_ID.value,  # noqa E501
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text"},
                        "value": "True",
                        "action_id": SlackUpsertCommandModalActionId.USER_SELECT_ENABLED_BUTTON.value,  # noqa E501
                    }
                ],
            },
        ),
        (
            True,
            {"user_select_enabled": False},
            {
                "block_id": SlackUpsertCommandModalBlockId.USER_SELECT_ENABLED_BLOCK_ID.value,  # noqa E501
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text"},
                        "value": "False",
                        "action_id": SlackUpsertCommandModalActionId.USER_SELECT_ENABLED_BUTTON.value,  # noqa E501
                    }
                ],
            },
        ),
        (
            True,
            {},
            {
                "type": "section",
                "block_id": SlackUpsertCommandModalBlockId.REMOVE_FROM_PICK_LIST_BLOCK_ID.value  # noqa E501
                + "_0",
                "text": {
                    "type": "mrkdwn",
                    "text": f"● {default_update_input_data['pick_list'][0]}",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":x:"},
                    "action_id": SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value,  # noqa E501
                },
            },
        ),
        (
            True,
            {},
            {
                "type": "section",
                "block_id": SlackUpsertCommandModalBlockId.REMOVE_FROM_PICK_LIST_BLOCK_ID.value  # noqa E501
                + "_1",
                "text": {
                    "type": "mrkdwn",
                    "text": f"● {default_update_input_data['pick_list'][1]}",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":x:"},
                    "action_id": SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value,  # noqa E501
                },
            },
        ),
        (
            True,
            {},
            {
                "type": "section",
                "block_id": SlackUpsertCommandModalBlockId.REMOVE_FROM_PICK_LIST_BLOCK_ID.value  # noqa E501
                + "_2",
                "text": {
                    "type": "mrkdwn",
                    "text": f"● {default_update_input_data['pick_list'][2]}",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":x:"},
                    "action_id": SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value,  # noqa E501
                },
            },
        ),
        (
            False,
            {},
            {
                "type": "input",
                "block_id": SlackUpsertCommandModalBlockId.STRATEGY_BLOCK_ID.value,
                "element": {
                    "type": "static_select",
                    "action_id": SlackUpsertCommandModalActionId.STRATEGY_SELECT.value,
                    "options": [
                        {
                            "value": Strategy.uniform.value,
                        },
                        {
                            "value": Strategy.smooth.value,
                        },
                        {
                            "value": Strategy.round_robin.value,
                        },
                    ],
                    "initial_option": [{"value": Strategy.uniform.value}],
                },
            },
        ),
        (
            True,
            {},
            {
                "type": "input",
                "block_id": SlackUpsertCommandModalBlockId.STRATEGY_BLOCK_ID.value,
                "element": {
                    "type": "static_select",
                    "action_id": SlackUpsertCommandModalActionId.STRATEGY_SELECT.value,
                    "options": [
                        {"value": Strategy.uniform.value},
                        {"value": Strategy.smooth.value},
                        {"value": Strategy.round_robin.value},
                    ],
                    "initial_option": [{"value": Strategy.smooth.value}],
                },
            },
        ),
        (
            False,
            {},
            {
                "type": "actions",
                "block_id": SlackUpsertCommandModalBlockId.CHECK_BOXES_BLOCK_ID.value,
                "elements": [
                    {
                        "type": "checkboxes",
                        "options": [{"value": "True"}],
                        "action_id": SlackUpsertCommandModalActionId.SELF_EXCLUDE_CHECKBOX.value,  # noqa E501
                    },
                    {
                        "type": "checkboxes",
                        "options": [{"value": "True"}],
                        "action_id": SlackUpsertCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value,  # noqa E501
                    },
                ],
            },
        ),
        (
            True,
            {},
            {
                "type": "actions",
                "block_id": SlackUpsertCommandModalBlockId.CHECK_BOXES_BLOCK_ID.value,
                "elements": [
                    {
                        "type": "checkboxes",
                        "options": [{"value": "True"}],
                        "initial_options": [{"value": "True"}],
                        "action_id": SlackUpsertCommandModalActionId.SELF_EXCLUDE_CHECKBOX.value,  # noqa E501
                    },
                    {
                        "type": "checkboxes",
                        "options": [{"value": "True"}],
                        "initial_options": [{"value": "True"}],
                        "action_id": SlackUpsertCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value,  # noqa E501
                    },
                ],
            },
        ),
    ],
)
def test_build_upsert_command_modal_blocks(upsert, input_data, expected_block):
    data = {**(default_update_input_data if upsert else {}), **input_data}
    modal = build_upsert_command_modal(upsert, team_id="1337", **data)
    assert_modal_has_expected_block(modal, expected_block)


def test_free_pick_list_input_does_not_exist_along_user_pick_list_input():
    modal = build_upsert_command_modal(False, team_id="1337", user_select_enabled=True)
    assert_modal_has_expected_block(
        modal,
        {"block_id": SlackUpsertCommandModalBlockId.USER_PICK_LIST_BLOCK_ID.value},
    )

    for block in modal["blocks"]:
        assert SlackUpsertCommandModalBlockId.FREE_PICK_LIST_BLOCK_ID.value not in block


def test_user_pick_list_input_does_not_exist_along_free_pick_list_input():
    modal = build_upsert_command_modal(False, team_id="1337", user_select_enabled=False)
    assert_modal_has_expected_block(
        modal,
        {"block_id": SlackUpsertCommandModalBlockId.FREE_PICK_LIST_BLOCK_ID.value},
    )

    for block in modal["blocks"]:
        assert SlackUpsertCommandModalBlockId.USER_PICK_LIST_BLOCK_ID.value not in block


def test_build_upsert_command_modal_metadata():
    modal = build_upsert_command_modal(
        True, team_id="1337", **default_update_input_data
    )
    expected_metadata = {
        "channel_id": default_update_input_data["previous_channel_id"],
        "pick_list": default_update_input_data["pick_list"],
        "user_select_enabled": default_update_input_data["user_select_enabled"],
        "command_name": default_update_input_data["command_name"],
    }
    match_object(json.loads(modal["private_metadata"]), expected_metadata)

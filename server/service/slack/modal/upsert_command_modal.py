import json
from enum import Enum

from server.service.slack.modal.enum import SlackModalSubmitAction
from server.service.slack.modal.pick_list_blocks import PickListBlocksFactory
from server.service.strategy.enum import Strategy


class SlackUpsertCommandModalActionId(Enum):
    CHANNEL_SELECT = "upsert_command_channel_select"
    COMMAND_NAME_INPUT = "upsert_command_command_name_input"
    DESCRIPTION_INPUT = "upsert_command_description_input"
    LABEL_INPUT = "upsert_command_label_input"
    USER_SELECT_ENABLED_BUTTON = "upsert_command_user_select_enabled_button"
    FREE_PICK_LIST_INPUT = "upsert_command_free_pick_list_input"
    USER_PICK_LIST_INPUT = "upsert_command_user_pick_list_input"
    REMOVE_FROM_PICK_LIST_BUTTON = "upsert_command_remove_from_pick_list_button"
    STRATEGY_SELECT = "upsert_command_strategy_select"
    SELF_EXCLUDE_CHECKBOX = "upsert_command_self_exclude_checkbox"
    ONLY_ACTIVE_USERS_CHECKBOX = "upsert_command_only_active_users_checkbox"


class SlackUpsertCommandModalBlockId(Enum):
    CHANNEL_BLOCK_ID = "channel_block_id"
    COMMAND_NAME_BLOCK_ID = "command_name_block_id"
    DESCRIPTION_BLOCK_ID = "description_label_block_id"
    LABEL_BLOCK_ID = "label_block_id"
    USER_SELECT_ENABLED_BLOCK_ID = "user_select_enabled_block_id"
    FREE_PICK_LIST_BLOCK_ID = "free_pick_list_block_id"
    USER_PICK_LIST_BLOCK_ID = "user_pick_list_block_id"
    REMOVE_FROM_PICK_LIST_BLOCK_ID = "remove_from_pick_list_block_id"
    STRATEGY_BLOCK_ID = "strategy_block_id"
    CHECK_BOXES_BLOCK_ID = "check_boxes_block_id"


SLACK_UPSERT_COMMAND_MODAL_VALUE_PATH = {
    SlackUpsertCommandModalActionId.CHANNEL_SELECT.value: f"{SlackUpsertCommandModalBlockId.CHANNEL_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.CHANNEL_SELECT.value}.selected_channel",  # noqa E501
    SlackUpsertCommandModalActionId.COMMAND_NAME_INPUT.value: f"{SlackUpsertCommandModalBlockId.COMMAND_NAME_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.COMMAND_NAME_INPUT.value}.value",  # noqa E501
    SlackUpsertCommandModalActionId.DESCRIPTION_INPUT.value: f"{SlackUpsertCommandModalBlockId.DESCRIPTION_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.DESCRIPTION_INPUT.value}.value",  # noqa E501
    SlackUpsertCommandModalActionId.LABEL_INPUT.value: f"{SlackUpsertCommandModalBlockId.LABEL_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.LABEL_INPUT.value}.value",  # noqa E501
    SlackUpsertCommandModalActionId.USER_SELECT_ENABLED_BUTTON.value: "",  # noqa E501
    SlackUpsertCommandModalActionId.FREE_PICK_LIST_INPUT.value: f"{SlackUpsertCommandModalActionId.FREE_PICK_LIST_INPUT.value}.value",  # noqa E501
    SlackUpsertCommandModalActionId.USER_PICK_LIST_INPUT.value: f"{SlackUpsertCommandModalActionId.USER_PICK_LIST_INPUT.value}.selected_user",  # noqa E501
    SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value: f"{SlackUpsertCommandModalBlockId.REMOVE_FROM_PICK_LIST_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value}.value",  # noqa E501
    SlackUpsertCommandModalActionId.STRATEGY_SELECT.value: f"{SlackUpsertCommandModalBlockId.STRATEGY_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.STRATEGY_SELECT.value}.selected_option.value",  # noqa E501
    SlackUpsertCommandModalActionId.SELF_EXCLUDE_CHECKBOX.value: f"{SlackUpsertCommandModalBlockId.CHECK_BOXES_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.SELF_EXCLUDE_CHECKBOX.value}.selected_options",  # noqa E501
    SlackUpsertCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value: f"{SlackUpsertCommandModalBlockId.CHECK_BOXES_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value}.selected_options",  # noqa E501
}

SLACK_UPSERT_COMMAND_ACTION_ID_TO_VARIABLE_NAME = {
    SlackUpsertCommandModalActionId.CHANNEL_SELECT.value: "channel_id",
    SlackUpsertCommandModalActionId.COMMAND_NAME_INPUT.value: "new_command_name",
    SlackUpsertCommandModalActionId.DESCRIPTION_INPUT.value: "description",
    SlackUpsertCommandModalActionId.LABEL_INPUT.value: "label",
    SlackUpsertCommandModalActionId.USER_SELECT_ENABLED_BUTTON.value: "user_select_enabled",  # noqa E501
    SlackUpsertCommandModalActionId.FREE_PICK_LIST_INPUT.value: "free_pick_list_item",
    SlackUpsertCommandModalActionId.USER_PICK_LIST_INPUT.value: "user_pick_list_item",
    SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value: "remove_from_pick_list_button",  # noqa E501
    SlackUpsertCommandModalActionId.STRATEGY_SELECT.value: "strategy",
    SlackUpsertCommandModalActionId.SELF_EXCLUDE_CHECKBOX.value: "self_exclude",
    SlackUpsertCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value: "only_active_users",
}


pick_list_blocks_factory = PickListBlocksFactory(
    SlackUpsertCommandModalActionId, SlackUpsertCommandModalBlockId
)


def build_header(upsert: bool, *, command_name: str = "") -> dict[str, any]:
    text = f"Update command {command_name}" if upsert else "Create a new command"
    return {
        "type": "modal",
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "title": {
            "type": "plain_text",
            "text": text,
            "emoji": True,
        },
        "close": {"type": "plain_text", "text": "Close", "emoji": True},
    }


def build_channel_select(channel_id: str) -> dict[str, any]:
    return {
        "type": "input",
        "block_id": SlackUpsertCommandModalBlockId.CHANNEL_BLOCK_ID.value,
        "label": {
            "type": "plain_text",
            "text": "Channel linked to the command",
        },
        "element": {
            "type": "channels_select",
            "placeholder": {"type": "plain_text", "text": "Channel", "emoji": True},
            "action_id": SlackUpsertCommandModalActionId.CHANNEL_SELECT.value,
            **({"initial_channel": channel_id} if channel_id else {}),
            "response_url_enabled": True,
        },
    }


def build_command_name_input(command_name: str) -> dict[str, any]:
    return {
        "type": "input",
        "block_id": SlackUpsertCommandModalBlockId.COMMAND_NAME_BLOCK_ID.value,
        "element": {
            "type": "plain_text_input",
            "placeholder": {
                "type": "plain_text",
                "text": "New command name",
                "emoji": True,
            },
            "initial_value": command_name if command_name else "",
            "action_id": SlackUpsertCommandModalActionId.COMMAND_NAME_INPUT.value,
        },
        "label": {
            "type": "plain_text",
            "text": "Name of the command",
            "emoji": True,
        },
    }


def build_description_input(description: str) -> dict[str, any]:
    return {
        "type": "input",
        "block_id": SlackUpsertCommandModalBlockId.DESCRIPTION_BLOCK_ID.value,
        "element": {
            "type": "plain_text_input",
            "multiline": True,
            "placeholder": {
                "type": "plain_text",
                "text": "A description to explain what this command does",
                "emoji": True,
            },
            "initial_value": description if description else "",
            "action_id": SlackUpsertCommandModalActionId.DESCRIPTION_INPUT.value,
        },
        "label": {
            "type": "plain_text",
            "text": "Extra information to describe the command",
            "emoji": True,
        },
        "optional": True,
    }


def build_label_input(label: str) -> dict[str, any]:
    return {
        "type": "input",
        "block_id": SlackUpsertCommandModalBlockId.LABEL_BLOCK_ID.value,
        "element": {
            "type": "plain_text_input",
            "multiline": True,
            "placeholder": {
                "type": "plain_text",
                "text": "Hey ! Someone choose something ...",
                "emoji": True,
            },
            "initial_value": label if label else "",
            "action_id": SlackUpsertCommandModalActionId.LABEL_INPUT.value,
        },
        "label": {
            "type": "plain_text",
            "text": "Extra text to add at the end of the pick message",
            "emoji": True,
        },
        "optional": True,
    }


def build_strategy_select(strategy_name: str) -> dict[str, any]:
    options = [
        {
            "text": {
                "type": "plain_text",
                "text": strategy.name,
                "emoji": True,
            },
            "value": strategy.name,
        }
        for strategy in Strategy
    ]

    initial_option = [option for option in options if option["value"] == strategy_name]
    initial_option = initial_option[0] if len(initial_option) else options[0]

    return {
        "type": "input",
        "block_id": SlackUpsertCommandModalBlockId.STRATEGY_BLOCK_ID.value,
        "element": {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Strategy",
                "emoji": True,
            },
            "action_id": SlackUpsertCommandModalActionId.STRATEGY_SELECT.value,
            "options": options,
            "initial_option": initial_option,
        },
        "label": {
            "type": "plain_text",
            "text": "Type of random strategy to use",
            "emoji": True,
        },
    }


def build_check_boxes(*, self_exclude: bool, only_active_users: bool) -> dict[str, any]:
    self_exclude_option = {
        "text": {
            "type": "plain_text",
            "text": "Should exclude the user that triggers the command ?",
            "emoji": True,
        },
        "value": "True",
    }
    only_active_users_option = {
        "text": {
            "type": "plain_text",
            "text": "Should only pick active users in the pick list ?",
            "emoji": True,
        },
        "value": "True",
    }

    return {
        "type": "actions",
        "block_id": SlackUpsertCommandModalBlockId.CHECK_BOXES_BLOCK_ID.value,
        "elements": [
            {
                "type": "checkboxes",
                "options": [self_exclude_option],
                **({"initial_options": [self_exclude_option]} if self_exclude else {}),
                "action_id": SlackUpsertCommandModalActionId.SELF_EXCLUDE_CHECKBOX.value,  # noqa E501
            },
            {
                "type": "checkboxes",
                "options": [only_active_users_option],
                **(
                    {"initial_options": [only_active_users_option]}
                    if only_active_users
                    else {}
                ),
                "action_id": SlackUpsertCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value,  # noqa E501
            },
        ],
    }


def build_upsert_command_modal(
    upsert: bool,
    *,
    team_id: str,
    channel_id: str = None,
    previous_channel_id: str = None,
    command_name: str = None,
    description: str = None,
    label: str = None,
    user_select_enabled: bool = True,
    pick_list: list[dict[str, any]] = None,
    free_pick_list_item: str = None,
    free_pick_list_input_block_id: str = None,
    strategy: str = None,
    self_exclude: bool = None,
    only_active_users: bool = None,
    **kwargs,
):
    modal_header = build_header(upsert)
    blocks = [
        build_channel_select(channel_id),
        build_command_name_input(command_name),
        build_description_input(description),
        build_label_input(label),
        *pick_list_blocks_factory.buld_pick_list_blocks(
            team_id=team_id,
            user_select_enabled=user_select_enabled,
            free_pick_list_item=free_pick_list_item,
            free_pick_list_input_block_id=free_pick_list_input_block_id,
            pick_list=pick_list,
        ),
        build_strategy_select(strategy),
        build_check_boxes(
            self_exclude=self_exclude, only_active_users=only_active_users
        ),
    ]

    action = (
        SlackModalSubmitAction.UPDATE_COMMAND.value
        if upsert
        else SlackModalSubmitAction.CREATE_COMMAND.value
    )

    return {
        **modal_header,
        "blocks": blocks,
        "callback_id": action,
        "private_metadata": json.dumps(
            {
                "channel_id": previous_channel_id or channel_id,
                "command_name": command_name,
                "pick_list": pick_list,
                "user_select_enabled": user_select_enabled,
            }
        ),
    }

from enum import Enum

from server.service.slack.message_formatting import get_user_id_from_mention
from server.service.slack.modal.enum import SlackModalSubmitAction


class SlackInstantCommandModalActionId(Enum):
    CHANNEL_SELECT = "channel_select"
    LABEL_INPUT = "label_input"
    PICK_LIST_INPUT = "pick_list_input"
    NUMBER_OF_ITEMS_INPUT = "number_of_items_input"
    ONLY_ACTIVE_USERS_CHECKBOX = "only_active_users_checkbox"


class SlackInstantCommandModalBlockId(Enum):
    CHANNEL_BLOCK_ID = "channel_block_id"
    LABEL_BLOCK_ID = "label_block_id"
    PICK_LIST_BLOCK_ID = "pick_list_block_id"
    NUMBER_OF_ITEMS_BLOCK_ID = "number_of_items_block_id"
    CHECK_BOXES_BLOCK_ID = "check_boxes_block_id"


SLACK_INSTANT_COMMAND_MODAL_VALUE_PATH = {
    SlackInstantCommandModalActionId.CHANNEL_SELECT.value: f"{SlackInstantCommandModalBlockId.CHANNEL_BLOCK_ID.value}.{SlackInstantCommandModalActionId.CHANNEL_SELECT.value}.selected_channel",  # noqa E501
    SlackInstantCommandModalActionId.LABEL_INPUT.value: f"{SlackInstantCommandModalBlockId.LABEL_BLOCK_ID.value}.{SlackInstantCommandModalActionId.LABEL_INPUT.value}.value",  # noqa E501
    SlackInstantCommandModalActionId.PICK_LIST_INPUT.value: f"{SlackInstantCommandModalBlockId.PICK_LIST_BLOCK_ID.value}.{SlackInstantCommandModalActionId.PICK_LIST_INPUT.value}.selected_users",  # noqa E501
    SlackInstantCommandModalActionId.NUMBER_OF_ITEMS_INPUT.value: f"{SlackInstantCommandModalBlockId.NUMBER_OF_ITEMS_BLOCK_ID.value}.{SlackInstantCommandModalActionId.NUMBER_OF_ITEMS_INPUT.value}.value",  # noqa E501
    SlackInstantCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value: f"{SlackInstantCommandModalBlockId.CHECK_BOXES_BLOCK_ID.value}.{SlackInstantCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value}.selected_options",  # noqa E501
}

SLACK_INSTANT_COMMAND_ACTION_ID_TO_VARIABLE_NAME = {
    SlackInstantCommandModalActionId.CHANNEL_SELECT.value: "channel_id",
    SlackInstantCommandModalActionId.LABEL_INPUT.value: "label",
    SlackInstantCommandModalActionId.PICK_LIST_INPUT.value: "pick_list",
    SlackInstantCommandModalActionId.NUMBER_OF_ITEMS_INPUT.value: "number_of_items_to_select",  # noqa E501
    SlackInstantCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value: "only_active_users",  # noqa E501
}


def build_header() -> dict[str, any]:
    text = "Run an intant command"
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
        "block_id": SlackInstantCommandModalBlockId.CHANNEL_BLOCK_ID.value,
        "label": {
            "type": "plain_text",
            "text": "Channel linked to the command",
        },
        "element": {
            "type": "channels_select",
            "placeholder": {"type": "plain_text", "text": "Channel", "emoji": True},
            "action_id": SlackInstantCommandModalActionId.CHANNEL_SELECT.value,
            **({"initial_channel": channel_id} if channel_id else {}),
            "response_url_enabled": True,
        },
    }


def build_label_input(label: str) -> dict[str, any]:
    return {
        "type": "input",
        "block_id": SlackInstantCommandModalBlockId.LABEL_BLOCK_ID.value,
        "element": {
            "type": "plain_text_input",
            "multiline": True,
            "placeholder": {
                "type": "plain_text",
                "text": "Hey ! Someone choose something ...",
                "emoji": True,
            },
            "initial_value": label if label else "",
            "action_id": SlackInstantCommandModalActionId.LABEL_INPUT.value,
        },
        "label": {
            "type": "plain_text",
            "text": "Extra text to add at the end of the pick message",
            "emoji": True,
        },
        "optional": True,
    }


def build_pick_list_input(pick_list: list[str]) -> dict[str, any]:
    initial_users = (
        [get_user_id_from_mention(user_mention) for user_mention in pick_list]
        if pick_list
        else []
    )
    return {
        "type": "input",
        "block_id": SlackInstantCommandModalBlockId.PICK_LIST_BLOCK_ID.value,
        "element": {
            "type": "multi_users_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Pick list",
                "emoji": True,
            },
            **({"initial_users": initial_users} if len(initial_users) else {}),
            "action_id": SlackInstantCommandModalActionId.PICK_LIST_INPUT.value,
        },
        "label": {
            "type": "plain_text",
            "text": "List of users from which to pick",
            "emoji": True,
        },
    }


def build_number_of_elements_input(number_of_items_to_select: int):
    return {
        "type": "input",
        "block_id": SlackInstantCommandModalBlockId.NUMBER_OF_ITEMS_BLOCK_ID.value,
        "label": {
            "type": "plain_text",
            "text": "Number of elements to pick",
            "emoji": True,
        },
        "element": {
            "type": "plain_text_input",
            "placeholder": {
                "type": "plain_text",
                "text": "Number between 1 and 50",
                "emoji": True,
            },
            "initial_value": number_of_items_to_select
            if number_of_items_to_select
            else "1",
            "action_id": SlackInstantCommandModalActionId.NUMBER_OF_ITEMS_INPUT.value,
        },
        "dispatch_action": False,
    }


def build_check_boxes(*, only_active_users: bool) -> dict[str, any]:
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
        "block_id": SlackInstantCommandModalBlockId.CHECK_BOXES_BLOCK_ID.value,
        "elements": [
            {
                "type": "checkboxes",
                "options": [only_active_users_option],
                **(
                    {"initial_options": [only_active_users_option]}
                    if only_active_users
                    else {}
                ),
                "action_id": SlackInstantCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value,  # noqa E501
            },
        ],
    }


def build_metadata(channel_id: str, command_name: str) -> str:
    return f'{{"channel_id": "{channel_id}", "command_name": "{command_name}"}}'


def build_instant_command_modal(
    *,
    channel_id: str = None,
    command_name: str = None,
    label: str = None,
    pick_list: list[str] = None,
    only_active_users: bool = None,
    number_of_items_to_select: int = None,
    **kwargs,
):
    modal_header = build_header()
    blocks = [
        build_channel_select(channel_id),
        build_label_input(label),
        build_pick_list_input(pick_list),
        build_number_of_elements_input(number_of_items_to_select),
        build_check_boxes(only_active_users=only_active_users),
    ]

    return {
        **modal_header,
        "blocks": blocks,
        "callback_id": SlackModalSubmitAction.RUN_INSTANT_COMMAND.value,
        "private_metadata": build_metadata(channel_id, command_name),
    }

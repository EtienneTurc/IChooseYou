import json
from datetime import datetime
from enum import Enum

from server.service.slack.message_formatting import get_user_id_from_mention
from server.service.slack.modal.enum import SlackModalSubmitAction
from server.service.strategy.enum import Strategy


class SlackUpsertCommandModalActionId(Enum):
    CHANNEL_SELECT = "channel_select"
    COMMAND_NAME_INPUT = "command_name_input"
    DESCRIPTION_INPUT = "description_input"
    LABEL_INPUT = "label_input"
    ONLY_USERS_IN_PICK_LIST_CHECKBOX = "only_users_in_pick_list_checkbox"
    FREE_PICK_LIST_INPUT = "free_pick_list_input"
    REMOVE_FROM_PICK_LIST_BUTTON = "remove_from_pick_list_button"
    USER_PICK_LIST_INPUT = "user_pick_list_input"
    STRATEGY_SELECT = "strategy_select"
    SELF_EXCLUDE_CHECKBOX = "self_exclude_checkbox"
    ONLY_ACTIVE_USERS_CHECKBOX = "only_active_users_checkbox"


class SlackUpsertCommandModalBlockId(Enum):
    CHANNEL_BLOCK_ID = "channel_block_id"
    COMMAND_NAME_BLOCK_ID = "command_name_block_id"
    DESCRIPTION_BLOCK_ID = "description_label_block_id"
    LABEL_BLOCK_ID = "label_block_id"
    ONLY_USERS_IN_PICK_LIST_BLOCK_ID = "only_users_in_pick_list_block_id"
    FREE_PICK_LIST_BLOCK_ID = "free_pick_list_block_id"
    REMOVE_FROM_PICK_LIST_BLOCK_ID = "remove_from_pick_list_block_id"
    USER_PICK_LIST_BLOCK_ID = "user_pick_list_block_id"
    STRATEGY_BLOCK_ID = "strategy_block_id"
    CHECK_BOXES_BLOCK_ID = "check_boxes_block_id"


SLACK_UPSERT_COMMAND_MODAL_VALUE_PATH = {
    SlackUpsertCommandModalActionId.CHANNEL_SELECT.value: f"{SlackUpsertCommandModalBlockId.CHANNEL_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.CHANNEL_SELECT.value}.selected_channel",  # noqa E501
    SlackUpsertCommandModalActionId.COMMAND_NAME_INPUT.value: f"{SlackUpsertCommandModalBlockId.COMMAND_NAME_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.COMMAND_NAME_INPUT.value}.value",  # noqa E501
    SlackUpsertCommandModalActionId.DESCRIPTION_INPUT.value: f"{SlackUpsertCommandModalBlockId.DESCRIPTION_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.DESCRIPTION_INPUT.value}.value",  # noqa E501
    SlackUpsertCommandModalActionId.LABEL_INPUT.value: f"{SlackUpsertCommandModalBlockId.LABEL_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.LABEL_INPUT.value}.value",  # noqa E501
    SlackUpsertCommandModalActionId.ONLY_USERS_IN_PICK_LIST_CHECKBOX.value: f"{SlackUpsertCommandModalBlockId.ONLY_USERS_IN_PICK_LIST_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.ONLY_USERS_IN_PICK_LIST_CHECKBOX.value}.selected_options",  # noqa E501
    SlackUpsertCommandModalActionId.FREE_PICK_LIST_INPUT.value: f"{SlackUpsertCommandModalActionId.FREE_PICK_LIST_INPUT.value}.value",  # noqa E501
    SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value: f"{SlackUpsertCommandModalBlockId.REMOVE_FROM_PICK_LIST_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value}.value",  # noqa E501
    SlackUpsertCommandModalActionId.USER_PICK_LIST_INPUT.value: f"{SlackUpsertCommandModalBlockId.USER_PICK_LIST_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.USER_PICK_LIST_INPUT.value}.selected_users",  # noqa E501
    SlackUpsertCommandModalActionId.STRATEGY_SELECT.value: f"{SlackUpsertCommandModalBlockId.STRATEGY_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.STRATEGY_SELECT.value}.selected_option.value",  # noqa E501
    SlackUpsertCommandModalActionId.SELF_EXCLUDE_CHECKBOX.value: f"{SlackUpsertCommandModalBlockId.CHECK_BOXES_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.SELF_EXCLUDE_CHECKBOX.value}.selected_options",  # noqa E501
    SlackUpsertCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value: f"{SlackUpsertCommandModalBlockId.CHECK_BOXES_BLOCK_ID.value}.{SlackUpsertCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value}.selected_options",  # noqa E501
}

SLACK_UPSERT_COMMAND_ACTION_ID_TO_VARIABLE_NAME = {
    SlackUpsertCommandModalActionId.CHANNEL_SELECT.value: "channel_id",
    SlackUpsertCommandModalActionId.COMMAND_NAME_INPUT.value: "new_command_name",
    SlackUpsertCommandModalActionId.DESCRIPTION_INPUT.value: "description",
    SlackUpsertCommandModalActionId.LABEL_INPUT.value: "label",
    SlackUpsertCommandModalActionId.ONLY_USERS_IN_PICK_LIST_CHECKBOX.value: "only_users_in_pick_list",  # noqa E501
    SlackUpsertCommandModalActionId.FREE_PICK_LIST_INPUT.value: "free_pick_list_item",
    SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value: "remove_from_pick_list_button",  # noqa E501
    SlackUpsertCommandModalActionId.USER_PICK_LIST_INPUT.value: "user_pick_list",
    SlackUpsertCommandModalActionId.STRATEGY_SELECT.value: "strategy",
    SlackUpsertCommandModalActionId.SELF_EXCLUDE_CHECKBOX.value: "self_exclude",
    SlackUpsertCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX.value: "only_active_users",
}


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


def build_only_users_in_pick_list_checkbox(
    only_users_in_pick_list: bool,
) -> dict[str, any]:
    only_users_in_pick_list_option = {
        "text": {
            "type": "plain_text",
            "text": "Should pick only users ?",
            "emoji": True,
        },
        "value": "True",
    }

    return {
        "type": "actions",
        "block_id": SlackUpsertCommandModalBlockId.ONLY_USERS_IN_PICK_LIST_BLOCK_ID.value,
        "elements": [
            {
                "type": "checkboxes",
                "options": [only_users_in_pick_list_option],
                **(
                    {"initial_options": [only_users_in_pick_list_option]}
                    if only_users_in_pick_list
                    else {}
                ),
                "action_id": SlackUpsertCommandModalActionId.ONLY_USERS_IN_PICK_LIST_CHECKBOX.value,  # noqa E501
            },
        ],
    }


def build_user_pick_list_input(pick_list: list[str]) -> dict[str, any]:
    initial_users = (
        [get_user_id_from_mention(user_mention) for user_mention in pick_list]
        if pick_list
        else []
    )
    return {
        "type": "input",
        "block_id": SlackUpsertCommandModalBlockId.USER_PICK_LIST_BLOCK_ID.value,
        "element": {
            "type": "users_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Pick list",
                "emoji": True,
            },
            **({"initial_users": initial_users} if len(initial_users) else {}),
            "action_id": SlackUpsertCommandModalActionId.USER_PICK_LIST_INPUT.value,
        },
        "label": {
            "type": "plain_text",
            "text": "List of users from which to pick",
            "emoji": True,
        },
    }


def build_free_pick_list_input(
    free_pick_list_item: str, block_id: str, optional: bool
) -> dict[str, any]:
    return {
        "type": "input",
        "block_id": block_id,
        "element": {
            "type": "plain_text_input",
            "action_id": SlackUpsertCommandModalActionId.FREE_PICK_LIST_INPUT.value,
            "placeholder": {
                "type": "plain_text",
                "text": "Element to add",
                "emoji": True,
            },
            "initial_value": free_pick_list_item if free_pick_list_item else "",
        },
        "label": {
            "type": "plain_text",
            "text": "Add elements to the pick list",
            "emoji": True,
        },
        "dispatch_action": True,
        "optional": optional,
    }


def build_free_pick_list_elements_display(pick_list: str) -> list[dict[str, any]]:
    if pick_list is None:
        return []

    sections = []
    for i, element in enumerate(pick_list):
        sections.append(
            {
                "type": "section",
                "block_id": SlackUpsertCommandModalBlockId.REMOVE_FROM_PICK_LIST_BLOCK_ID.value  # noqa E501
                + f"_{i}",
                "text": {"type": "mrkdwn", "text": f"● {element}"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":x:", "emoji": True},
                    "action_id": SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value,  # noqa E501
                },
            }
        )
    return sections


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


def build_metadata(
    channel_id: str,
    command_name: str,
    user_pick_list: list[str],
    free_pick_list: list[str],
) -> str:
    return json.dumps(
        {
            "channel_id": channel_id,
            "command_name": command_name,
            "user_pick_list": user_pick_list,
            "free_pick_list": free_pick_list,
        }
    )


def build_pick_list_input_section(
    only_users_in_pick_list: bool,
    user_pick_list: list[str],
    free_pick_list: list[str],
    free_pick_list_item: str,
    free_pick_list_input_block_id: str = None,
):
    if only_users_in_pick_list:
        return [build_user_pick_list_input(user_pick_list)]

    if not free_pick_list_input_block_id:
        free_pick_list_input_block_id = (
            SlackUpsertCommandModalBlockId.FREE_PICK_LIST_BLOCK_ID.value
            + "_"
            + str(datetime.timestamp(datetime.now()))
        )

    return [
        build_free_pick_list_input(
            free_pick_list_item,
            free_pick_list_input_block_id,
            free_pick_list is not None and len(free_pick_list) != 0,
        ),
        *build_free_pick_list_elements_display(free_pick_list),
    ]


def build_upsert_command_modal(
    upsert: bool,
    *,
    channel_id: str = None,
    previous_channel_id: str = None,
    command_name: str = None,
    description: str = None,
    label: str = None,
    only_users_in_pick_list: bool = True,
    user_pick_list: list[str] = None,
    free_pick_list: list[str] = None,
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
        build_only_users_in_pick_list_checkbox(only_users_in_pick_list),
        *build_pick_list_input_section(
            only_users_in_pick_list,
            user_pick_list,
            free_pick_list,
            free_pick_list_item,
            free_pick_list_input_block_id,
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
        "private_metadata": build_metadata(
            previous_channel_id or channel_id,
            command_name,
            user_pick_list,
            free_pick_list,
        ),
    }

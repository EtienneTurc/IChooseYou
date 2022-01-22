from enum import Enum

from server.service.slack.helper import format_callback_id
from server.service.slack.modal.enum import SlackModalSubmitAction


class SlackCustomCommandModalActionId(Enum):
    ADDITIONAL_TEXT_INPUT = "additional_text_input"
    NUMBER_OF_ITEMS_INPUT = "number_of_items_input"


class SlackCustomCommandModalBlockId(Enum):
    ADDITIONAL_TEXT_BLOCK_ID = "additional_text_block_id"
    NUMBER_OF_ITEMS_BLOCK_ID = "number_of_items_block_id"


SLACK_CUSTOM_COMMAND_MODAL_VALUE_PATH = {
    SlackCustomCommandModalActionId.ADDITIONAL_TEXT_INPUT.value: f"{SlackCustomCommandModalBlockId.ADDITIONAL_TEXT_BLOCK_ID.value}.{SlackCustomCommandModalActionId.ADDITIONAL_TEXT_INPUT.value}.value",  # noqa E501
    SlackCustomCommandModalActionId.NUMBER_OF_ITEMS_INPUT.value: f"{SlackCustomCommandModalBlockId.NUMBER_OF_ITEMS_BLOCK_ID.value}.{SlackCustomCommandModalActionId.NUMBER_OF_ITEMS_INPUT.value}.value",  # noqa E501
}

SLACK_CUSTOM_COMMAND_ACTION_ID_TO_VARIABLE_NAME = {
    SlackCustomCommandModalActionId.ADDITIONAL_TEXT_INPUT.value: "additional_text",
    SlackCustomCommandModalActionId.NUMBER_OF_ITEMS_INPUT.value: "number_of_items_to_select",  # noqa E501
}


def build_header(command_name: str):
    return {
        "type": "modal",
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "title": {
            "type": "plain_text",
            "text": f"{command_name}",
            "emoji": True,
        },
        "close": {"type": "plain_text", "text": "Close", "emoji": True},
    }


def build_additional_text_input(additional_text: str):
    return {
        "type": "input",
        "block_id": SlackCustomCommandModalBlockId.ADDITIONAL_TEXT_BLOCK_ID.value,
        "element": {
            "type": "plain_text_input",
            "multiline": True,
            "placeholder": {
                "type": "plain_text",
                "text": "Hey ! I choose you to ...",
            },
            "action_id": SlackCustomCommandModalActionId.ADDITIONAL_TEXT_INPUT.value,
            "initial_value": additional_text if additional_text else "",
        },
        "label": {
            "type": "plain_text",
            "text": "Additional text to display",
            "emoji": True,
        },
        "optional": True,
        "dispatch_action": False,
    }


def build_number_of_elements_input(
    size_of_pick_list: int, number_of_items_to_select: int
):
    return {
        "type": "input",
        "block_id": SlackCustomCommandModalBlockId.NUMBER_OF_ITEMS_BLOCK_ID.value,
        "label": {
            "type": "plain_text",
            "text": f"Number of elements to pick ({size_of_pick_list} elements in the pick list)",  # noqa E501
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
            "action_id": SlackCustomCommandModalActionId.NUMBER_OF_ITEMS_INPUT.value,
        },
        "dispatch_action": False,
    }


def build_custom_command_modal(
    *,
    command_id: int,
    command_name: str,
    size_of_pick_list: int,
    additional_text: str = None,
    number_of_items_to_select: int = None,
    **kwargs,
):
    modal_header = build_header(command_name)
    blocks = [
        build_additional_text_input(additional_text),
        build_number_of_elements_input(size_of_pick_list, number_of_items_to_select),
    ]
    callback_id = format_callback_id(
        SlackModalSubmitAction.RUN_CUSTOM_COMMAND.value, command_id
    )

    return {**modal_header, "blocks": blocks, "callback_id": callback_id}

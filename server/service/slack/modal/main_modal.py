from flask import current_app

from server.orm.command import Command
from server.service.helper.list_helper import flatten
from server.service.slack.modal.enum import (SlackMainModalActionId,
                                             SlackMainModalOverflowActionId)


def build_main_modal_header():
    return {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": current_app.config["APP_NAME"],
            "emoji": True,
        },
        "close": {"type": "plain_text", "text": "Close", "emoji": True},
    }


def build_create_command_section():
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":hammer: *Create a new command*",
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Add",
                "emoji": True,
            },
            "style": "primary",
            "action_id": SlackMainModalActionId.CREATE_NEW_COMMAND.value,
        },
    }


def build_command_section(command: Command) -> list[dict[str, any]]:
    return [
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": build_command_text(command),
            },
            "accessory": {
                "type": "overflow",
                "options": build_overflow_options(str(command["_id"])),
                "action_id": SlackMainModalActionId.MANAGE_COMMAND.value,
            },
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":rocket:               Run               :rocket:",
                        "emoji": True,
                    },
                    "action_id": SlackMainModalActionId.SELECT_COMMAND.value,
                    "value": str(command["_id"]),
                },
            ],
        },
    ]


def build_overflow_options(command_id: str) -> list[dict[str, any]]:
    return [
        {
            "text": {
                "type": "plain_text",
                "text": ":hammer_and_wrench:   Update",
                "emoji": True,
            },
            "value": f"{SlackMainModalOverflowActionId.UPDATE_COMMAND.value}.{command_id}",  # noqa E501
        },
        {
            "text": {
                "type": "plain_text",
                "text": ":x:   Delete",
                "emoji": True,
            },
            "value": f"{SlackMainModalOverflowActionId.DELETE_COMMAND.value}.{command_id}",  # noqa E501
        },
    ]


def build_command_text(command: Command) -> str:
    name = f"*{command['name']}*"
    description = (
        command["description"]
        if command.get("description")
        else "_No description provided_ :smiling_face_with_tear:"
    )
    return f"{name}\n{description}"


def build_metadata(channel_id: str) -> str:
    return f'{{"channel_id": "{channel_id}"}}'


def build_main_modal(*, channel_id: str, commands: list[Command], **kwargs):
    modal_header = build_main_modal_header()
    blocks = [
        build_create_command_section(),
        *flatten([build_command_section(command) for command in commands]),
    ]

    return {
        **modal_header,
        "blocks": blocks,
        "private_metadata": build_metadata(channel_id),
    }
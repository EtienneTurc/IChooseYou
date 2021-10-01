from flask import current_app

from server.orm.command import Command

from enum import Enum


class SlackMainModalActionId(Enum):
    CREATE_NEW_COMMAND = "create_new_command"
    SELECT_COMMAND = "select_command"


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
            "text": {"type": "plain_text", "text": "Add", "emoji": True},
            "style": "primary",
            "action_id": SlackMainModalActionId.CREATE_NEW_COMMAND.value,
        },
    }


def build_command_section(command: Command):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": build_command_text(command),
        },
        "accessory": {
            "type": "button",
            "text": {"type": "plain_text", "text": "Run", "emoji": True},
            "action_id": SlackMainModalActionId.SELECT_COMMAND.value,
            "value": str(command._id),
        },
    }


def build_command_text(command: Command) -> str:
    name = f"*{command.name}*"
    description = "Description of my command Description of my command Description of my command Description of my command Description of my command"
    update = "<google.com|update>"
    delete = "<google.com|delete>"
    return f"{name}\n{description}\n{update} | {delete}"


def build_main_modal(*, commands: list[Command], **kwargs):
    modal_header = build_main_modal_header()
    blocks = [
        build_create_command_section(),
        {"type": "divider"},
        *[build_command_section(command) for command in commands],
    ]

    return {**modal_header, "blocks": blocks}

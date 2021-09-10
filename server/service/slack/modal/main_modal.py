from flask import current_app

from server.orm.command import Command


def build_main_modal_header():
    return {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": current_app.config["APP_NAME"],
            "emoji": True,
        },
    }


def build_manage_section():
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":hammer: *Create, update or delete existing command*",
        },
        "accessory": {
            "type": "button",
            "text": {"type": "plain_text", "text": "Manage", "emoji": True},
            "style": "primary",
            "value": "click_me_123",
        },
    }


def build_command_section(command: Command):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*{command.name}*",
        },
        "accessory": {
            "type": "button",
            "text": {"type": "plain_text", "text": "Execute", "emoji": True},
            "style": "primary",
            "value": "click_me_123",
            "action_id": "execute",
        },
    }


def build_main_modal(*, commands: list[Command], **kwargs):
    modal_header = build_main_modal_header()
    blocks = [
        build_manage_section(),
        {"type": "divider"},
        *[build_command_section(command) for command in commands],
    ]

    return {**modal_header, "blocks": blocks}

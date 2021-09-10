from flask import current_app


def build_header_main_modal():
    return

def build_main_modal():


modal = {
    "type": "modal",
    "submit": {"type": "plain_text", "text": "Submit", "emoji": true},
    "title": {
        "type": "plain_text",
        "text": current_app.config["APP_NAME"],
        "emoji": true,
    },
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":hammer: *Create command*",
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Create", "emoji": true},
                "style": "primary",
                "value": "click_me_123",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":hammer_and_wrench: *Update command*",
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Update", "emoji": true},
                "style": "primary",
                "value": "click_me_123",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":broom: *Delete command*",
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Delete", "emoji": true},
                "style": "primary",
                "value": "click_me_123",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*cr*",
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Execute", "emoji": true},
                "style": "primary",
                "value": "click_me_123",
            },
        },
    ],
}

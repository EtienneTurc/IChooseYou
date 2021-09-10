modal = {
    "type": "modal",
    "submit": {"type": "plain_text", "text": "Submit", "emoji": true},
    "title": {
        "type": "plain_text",
        "text": "Run command test_main_modal",
        "emoji": true,
    },
    "blocks": [
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "multiline": true,
                "action_id": "plain_text_input-action",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Hey ! I choose you to ...",
                },
            },
            "label": {
                "type": "plain_text",
                "text": "Additional text to display",
                "emoji": true,
            },
            "optional": true,
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Number of elements to pick"},
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                    "emoji": true,
                },
                "options": [
                    {
                        "text": {"type": "plain_text", "text": "1", "emoji": true},
                        "value": "1",
                    },
                    {
                        "text": {"type": "plain_text", "text": "2", "emoji": true},
                        "value": "2",
                    },
                    {
                        "text": {"type": "plain_text", "text": "3", "emoji": true},
                        "value": "3",
                    },
                ],
                "initial_option": {
                    "text": {"type": "plain_text", "text": "1", "emoji": true},
                    "value": "1",
                },
                "action_id": "static_select-action",
            },
        },
    ],
    "callback_id": "run_custom_command.610e840da9ef2bd3e947941a",
}

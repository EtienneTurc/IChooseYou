from flask import current_app

from server.service.slack.workflow.enum import WorkflowActionId, WorkflowBlockId


def build_send_to_slack_check_box(send_to_slack_enabled):
    text = "Send message to slack.\n"
    text += "If disabled, it will only expose the result of the command"
    text += " for the next workflow."

    checkbox_options = [
        {
            "text": {
                "type": "plain_text",
                "text": text,
                "emoji": True,
            },
            "value": "True",
        }
    ]
    return {
        "type": "input",
        "block_id": WorkflowBlockId.SEND_TO_SLACK_CHECKBOX.value,
        "element": {
            "type": "checkboxes",
            "options": checkbox_options,
            **({"initial_options": checkbox_options} if send_to_slack_enabled else {}),
            "action_id": WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value,
        },
        "label": {
            "type": "plain_text",
            "text": "Send to slack ?",
            "emoji": True,
        },
        "optional": True,
    }


def build_workflow_edit_modal(
    initial_channel: str, initial_command: str, send_to_slack_enabled: bool
):
    return {
        "type": "workflow_step",
        "blocks": [
            {
                "type": "input",
                "block_id": WorkflowBlockId.CHANNEL_INPUT.value,
                "element": {
                    "type": "conversations_select",
                    "action_id": WorkflowActionId.CHANNEL_INPUT.value,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a channel",
                        "emoji": True,
                    },
                    **(
                        {"initial_conversation": initial_channel}
                        if initial_channel
                        else {}
                    ),
                    "filter": {
                        "include": ["public", "private"],
                        "exclude_bot_users": True,
                        "exclude_external_shared_channels": True,
                    },
                },
                "label": {
                    "type": "plain_text",
                    "text": "Channel using the slash command",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "block_id": WorkflowBlockId.COMMAND_INPUT.value,
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": WorkflowActionId.COMMAND_INPUT.value,
                    "placeholder": {
                        "type": "plain_text",
                        "text": f"{current_app.config['SLASH_COMMAND']} my_command with_my_extra_text",  # noqa E501
                        "emoji": True,
                    },
                    **({"initial_value": initial_command} if initial_command else {}),
                },
                "label": {
                    "type": "plain_text",
                    "text": "Slash command to execute",
                    "emoji": True,
                },
            },
            build_send_to_slack_check_box(send_to_slack_enabled),
        ],
    }

import json

from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.responder.enum import SlackResubmitButtonsActionId
from server.service.slack.response.api_response import (send_built_message_to_channel,
                                                        send_message_to_channel)


def send_message_to_channel_with_resubmit_button_and_info(
    *,
    message: Message,
    channel_id: str,
    user_id: str = None,
    team_id: str,
    command_name: str,
    additional_text: str,
    number_of_items_to_select: int,
    **kwargs
):
    slack_message = send_message_to_channel(
        message=message, channel_id=channel_id, user_id=user_id, team_id=team_id
    )

    # Send resubmit message
    resubmit_payload = build_resubmit_payload_payload(
        command_name=command_name,
        additional_text=additional_text,
        number_of_items_to_select=number_of_items_to_select,
    )
    send_built_message_to_channel(
        payload=resubmit_payload,
        visibility=MessageVisibility.HIDDEN,
        channel_id=channel_id,
        user_id=user_id,
        team_id=team_id,
        thread_ts=slack_message.get("ts"),
    )

    # Send info message
    send_message_to_channel(
        message=Message(
            content="Info about the command comming soon",
            visibility=MessageVisibility.NORMAL.value,
        ),
        channel_id=channel_id,
        team_id=team_id,
        thread_ts=slack_message.get("ts"),
    )


def build_resubmit_payload_payload(
    *, command_name: str, additional_text: str, number_of_items_to_select: int
):
    button_value = json.dumps(
        {
            "command_name": command_name,
            "additional_text": additional_text,
            "number_of_items_to_select": number_of_items_to_select,
        }
    )

    blocks = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Update & Resubmit",
                        "emoji": True,
                    },
                    "action_id": SlackResubmitButtonsActionId.UPDATE_AND_RESUBMIT_COMMAND.value,  # noqa E501
                    "value": button_value,
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Resubmit",
                        "emoji": True,
                    },
                    "action_id": SlackResubmitButtonsActionId.RESUBMIT_COMMAND.value,
                    "value": button_value,
                },
            ],
        }
    ]

    return {
        "text": "",
        "attachments": [
            {
                "color": MessageStatus.INFO.value,
                "blocks": blocks,
            }
        ],
    }

import json
import time

from server.service.helper.dict_helper import get_by_path
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.responder.enum import SlackResubmitButtonsActionId
from server.service.slack.response.api_response import (send_built_message_to_channel,
                                                        send_file_to_channel,
                                                        send_message_to_channel)
from server.service.wheel.image_helper import save_gif


def send_message_and_gif_to_channel_with_resubmit_button(
    *,
    channel_id: str,
    team_id: str,
    user_id: str,
    gif_frames: list[any],
    with_wheel: bool,
    **kwargs,
):
    wheel_ts = None
    if with_wheel:
        send_message_to_channel(
            message=Message(
                content="Spin that wheel :ferris_wheel:",
                visibility=MessageVisibility.HIDDEN,
            ),
            channel_id=channel_id,
            user_id=user_id,
            team_id=team_id,
        )
        with open("wheel.gif", "wb") as file_pointer:
            save_gif(file_pointer, gif_frames)
            message_response = send_file_to_channel(
                channel_id=channel_id, file_pointer=file_pointer.name, team_id=team_id
            )
            wheel_ts = (
                get_by_path(message_response.data, f"file.shares.public.{channel_id}")
                or get_by_path(
                    message_response.data, f"file.shares.private.{channel_id}"
                )
            )[0]["ts"]
            time.sleep(5)  # Sleep for 5 seconds

    kwargs["wheel_ts"] = wheel_ts  # Overwrite previous value
    send_message_to_channel_with_resubmit_button(
        channel_id=channel_id,
        team_id=team_id,
        with_wheel=with_wheel,
        user_id=user_id,
        **kwargs,
    )


def send_message_to_channel_with_resubmit_button(
    *,
    message: Message,
    channel_id: str,
    user_id: str = None,
    team_id: str,
    command_name: str,
    additional_text: str,
    number_of_items_to_select: int,
    with_wheel: bool,
    wheel_ts: str,
    **kwargs,
):
    message_response = send_message_to_channel(
        message=message, channel_id=channel_id, user_id=user_id, team_id=team_id
    )

    # Send resubmit message
    resubmit_payload = build_resubmit_payload_payload(
        command_name=command_name,
        additional_text=additional_text,
        number_of_items_to_select=number_of_items_to_select,
        with_wheel=with_wheel,
        message_text=message.content,
        ts=message_response.data.get("ts"),
        wheel_ts=wheel_ts,
    )
    send_built_message_to_channel(
        payload=resubmit_payload,
        visibility=MessageVisibility.HIDDEN,
        channel_id=channel_id,
        user_id=user_id,
        team_id=team_id,
    )


def build_resubmit_payload_payload(
    *,
    command_name: str,
    additional_text: str,
    number_of_items_to_select: int,
    with_wheel: bool,
    message_text: str,
    ts: str,
    wheel_ts: str,
):
    button_value = {
        "command_name": command_name,
        "additional_text": additional_text,
        "number_of_items_to_select": number_of_items_to_select,
        "with_wheel": with_wheel,
    }

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
                    "value": json.dumps(button_value),
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Resubmit",
                        "emoji": True,
                    },
                    "action_id": SlackResubmitButtonsActionId.RESUBMIT_COMMAND.value,
                    "value": json.dumps(button_value),
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Resubmit & Delete message",
                        "emoji": True,
                    },
                    "action_id": SlackResubmitButtonsActionId.RESUBMIT_COMMAND_AND_DELETE_MESSAGE.value,  # noqa E501
                    "value": json.dumps(
                        {
                            **button_value,
                            "message_text": message_text,
                            "ts": ts,
                            "wheel_ts": wheel_ts,
                        }
                    ),
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

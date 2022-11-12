from marshmallow import ValidationError

from server.service.error.logger import log_error
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.response.api_response import (
    send_message_to_channel, send_message_to_channel_via_response_url)


def on_error_handled_send_message(
    error: Exception,
    *,
    request: dict[str, any],
    response_url: str = None,
    channel_id: str = None,
    team_id: str = None,
    user_id: str = None,
    **kwargs,
) -> None:
    log_error(
        error=error,
        request=request,
        team_id=team_id,
        user_id=user_id,
        channel_id=channel_id,
    )

    error_message = error
    if type(error) is ValidationError:
        error_message = format_validation_error(error)

    message = Message(
        content=f"{error_message}",
        status=MessageStatus.LIGHT_ERROR,
        visibility=MessageVisibility.HIDDEN,
    )

    if response_url:
        return send_message_to_channel_via_response_url(
            message=message, response_url=response_url
        )

    return send_message_to_channel(
        message=message, channel_id=channel_id, team_id=team_id, user_id=user_id
    )


def format_validation_error(error):
    message = ""
    for key, error_message in error.messages.items():
        message += f"Field '{key}' is not valid. Failed with error: {error_message}.\n"
    return message[:-2]

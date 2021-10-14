import traceback


from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.response.api_response import (
    send_message_to_channel,
    send_message_to_channel_via_response_url,
)


def on_error_handled_send_message(
    error: Exception,
    *,
    response_url: str = None,
    channel_id: str = None,
    team_id: str = None,
    **kwargs,
) -> None:
    traceback.print_exc()  # Print stacktrace

    message = Message(
        content=f"{error}",
        status=MessageStatus.LIGHT_ERROR,
        visibility=MessageVisibility.HIDDEN,
    )

    if response_url:
        return send_message_to_channel_via_response_url(
            message=message, response_url=response_url
        )

    return send_message_to_channel(
        message=message, channel_id=channel_id, team_id=team_id
    )

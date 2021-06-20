import traceback

from marshmallow import ValidationError

from server.service.command.args import ArgError
from server.service.error.back_error import BackError
from server.service.helper.dict_helper import pick
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.sdk_wrapper import send_message_to_channel


def error_handler(
    error: str, error_status: int, *, channel_id: str, team_id: str, user_id: str
) -> None:
    traceback.print_exc()  # Print stacktrace

    message = Message(
        content=f"{error}",
        status=MessageStatus.LIGHT_ERROR
        if error_status == 400
        else MessageStatus.ERROR,
        visibility=MessageVisibility.HIDDEN,
    )

    return send_message_to_channel(
        message, channel_id=channel_id, team_id=team_id, user_id=user_id
    )


def handle_error(func):
    def handle_error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ArgError as error:
            return error_handler(
                error, 400, **pick(kwargs, ["channel_id", "team_id", "user_id"])
            )
        except ValidationError as error:
            return error_handler(
                error, 400, **pick(kwargs, ["channel_id", "team_id", "user_id"])
            )
        except BackError as error:
            return error_handler(
                error,
                error.status,
                **pick(kwargs, ["channel_id", "team_id", "user_id"]),
            )
        except Exception as error:
            return error_handler(
                error, 500, **pick(kwargs, ["channel_id", "team_id", "user_id"])
            )

    return handle_error_wrapper

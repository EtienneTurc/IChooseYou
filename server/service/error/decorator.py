import traceback

from marshmallow import ValidationError

from server.service.command.args import ArgError
from server.service.error.back_error import BackError
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.sdk_wrapper import send_message_to_channel_via_response_url


def error_handler(error: str, error_status: int, *, response_url: str) -> None:
    traceback.print_exc()  # Print stacktrace

    message = Message(
        content=f"{error}",
        status=MessageStatus.LIGHT_ERROR
        if error_status == 400
        else MessageStatus.ERROR,
        visibility=MessageVisibility.HIDDEN,
    )

    return send_message_to_channel_via_response_url(message, response_url)


def handle_error(func):
    def handle_error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ArgError as error:
            return error_handler(error, 400, response_url=kwargs.get("response_url"))
        except ValidationError as error:
            return error_handler(error, 400, response_url=kwargs.get("response_url"))
        except BackError as error:
            return error_handler(
                error,
                error.status,
                response_url=kwargs.get("response_url"),
            )
        except Exception as error:
            return error_handler(error, 500, response_url=kwargs.get("response_url"))

    return handle_error_wrapper

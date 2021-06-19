import traceback

from marshmallow import ValidationError

from server.service.command.args import ArgError
from server.service.error.back_error import BackError
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.response import send_to_channel


def error_handler(error, error_status, response_url):
    traceback.print_exc()  # Print stacktrace

    message = Message(
        content=f"{error}",
        status=MessageStatus.LIGHT_ERROR
        if error_status == 400
        else MessageStatus.ERROR,
        visibility=MessageVisibility.HIDDEN,
    )

    return send_to_channel(message, response_url)


def handle_error(func):
    def handle_error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ArgError as error:
            return error_handler(error, 400, kwargs["response_url"])
        except ValidationError as error:
            return error_handler(error, 400, kwargs["response_url"])
        except BackError as error:
            return error_handler(error, error.status, kwargs["response_url"])
        except Exception as error:
            return error_handler(error, 500, kwargs["response_url"])

    return handle_error_wrapper

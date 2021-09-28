import traceback

from marshmallow import ValidationError

from server.service.command.args import ArgError
from server.service.error.back_error import BackError
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.sdk_wrapper import (
    failed_worklow,
    send_message_to_channel_via_response_url,
)
from server.service.error.mapping import ERROR_TO_RESPONSE_ACTION


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


def workflow_error_handler(
    error: str, *, workflow_step_execute_id: str, team_id
) -> None:
    traceback.print_exc()  # Print stacktrace

    return failed_worklow(error, workflow_step_execute_id, team_id)


def handle_workflow_error(func):
    def handle_error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return workflow_error_handler(
                error.message,
                workflow_step_execute_id=kwargs.get("workflow_step_execute_id"),
                team_id=kwargs.get("team_id"),
            )

    return handle_error_wrapper


def tpr_handle_error(func):
    def tpr_handle_error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return ERROR_TO_RESPONSE_ACTION[type(error)](**kwargs)

    return tpr_handle_error_wrapper

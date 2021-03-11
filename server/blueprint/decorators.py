import traceback

from flask import make_response, request
from marshmallow import ValidationError
from slack_sdk.webhook import WebhookClient

from server.blueprint.back_error import BackError
from server.command.args import ArgError
from server.slack.message_status import MessageStatus, MessageVisibility
from server.slack.utils import slack_signature_validation


def error_handler(error, error_status):
    traceback.print_exc()  # Print stacktrace

    def sendError(error, error_status):
        return (
            f"{error}",
            MessageStatus.LIGHT_ERROR if error_status == 400 else MessageStatus.ERROR,
            MessageVisibility.HIDDEN,
        )

    return send_return(sendError)(error, error_status)


def handle_error(func):
    def handle_error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ArgError as error:
            return error_handler(error, 400)
        except ValidationError as error:
            return error_handler(error, 400)
        except BackError as error:
            return error_handler(error, error.status)
        except Exception as error:
            return error_handler(error, 500)

    return handle_error_wrapper


def format_body(func):
    def format_wrapper(*args, **kwargs):
        channel = {
            "id": request.form.get("channel_id"),
            "name": request.form.get("channel_name"),
        }
        user = {
            "id": request.form.get("user_id"),
            "name": request.form.get("user_name"),
        }
        text = request.form.get("text")
        command_name = text.split(" ")[0]
        text = " ".join(text.split(" ")[1:])
        response_url = request.form.get("response_url")

        return func(
            channel=channel,
            user=user,
            command_name=command_name,
            text=text,
            response_url=response_url,
        )

    return format_wrapper


def validate(schema):
    def validate_decorator(func):
        def validate_wrapper(*args, **kwargs):
            slack_signature_validation(request)
            schema().load(kwargs)
            return func(**kwargs)

        return validate_wrapper

    return validate_decorator


def send_return(func):
    def send_return_wrapper(*args, **kwargs):
        message, message_status, message_visibility = func(*args, **kwargs)

        webhook = WebhookClient(request.form["response_url"])
        webhook.send(
            text="",
            response_type=message_visibility.value
            if message_visibility
            else MessageVisibility.HIDDEN,
            replace_original=True,
            attachments=[
                {
                    "color": message_status.value
                    if message_status
                    else MessageStatus.INFO,
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"{message}",
                            },
                        }
                    ],
                }
            ],
        )
        return make_response("", 200)

    return send_return_wrapper

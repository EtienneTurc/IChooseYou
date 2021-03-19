import traceback

from flask import make_response, request
from marshmallow import ValidationError
from slack_sdk.webhook import WebhookClient

from server.blueprint.back_error import BackError
from server.command.args import ArgError
from server.slack.message_status import MessageStatus, MessageVisibility
from server.slack.utils import slack_signature_valid


def make_context(func):
    def make_context_wrapper(app, *args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)

    return make_context_wrapper


def error_handler(error, error_status, response_url):
    traceback.print_exc()  # Print stacktrace

    def sendError(error, error_status, **kwargs):
        return (
            f"{error}",
            MessageStatus.LIGHT_ERROR if error_status == 400 else MessageStatus.ERROR,
            MessageVisibility.HIDDEN,
        )

    return send_to_channel(sendError)(error, error_status, response_url=response_url)


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
        team_id = request.form.get("team_id")

        return func(
            channel=channel,
            user=user,
            command_name=command_name,
            text=text,
            response_url=response_url,
            team_id=team_id,
        )

    return format_wrapper


def validate_signature(func):
    def validate_signature_wrapper(*args, **kwargs):
        if not slack_signature_valid(request):
            return make_response("invalid request", 403)
        return func(*args, **kwargs)

    return validate_signature_wrapper


def validate(schema):
    def validate_decorator(func):
        def validate_wrapper(*args, **kwargs):
            schema().load(kwargs)
            return func(**kwargs)

        return validate_wrapper

    return validate_decorator


def send_to_channel(func):
    def send_to_channel_wrapper(*args, **kwargs):
        message, message_status, message_visibility = func(*args, **kwargs)

        webhook = WebhookClient(kwargs["response_url"])
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

    return send_to_channel_wrapper

from flask import Blueprint, make_response, request
from slack_sdk.webhook import WebhookClient

from server.command.help import KNOWN_COMMANDS, KNOWN_COMMANDS_NAMES
from server.command.custom import CustomCommand
from server.orm.command import Command
from server.slack.utils import error_handler, format_slack_request, webhook_send_message
from server.command.args import ArgError
from server.slack.validator import check_incoming_request_is_valid


from server.slack.message_status import MessageStatus

slack_webhook = Blueprint("slack_webhook", __name__, url_prefix="/slack_webhook")


@slack_webhook.route("/", methods=["POST"])
def slack_app():
    check_incoming_request_is_valid(request)
    channel, user, command_name, text, response_url = format_slack_request(request)
    webhook = WebhookClient(response_url)

    try:
        if not command_name:
            message = "No command found.\n"
            message += (
                "You see different commands ans their usage with the help command."
            )
            webhook_send_message(webhook, message, MessageStatus.LIGHT_ERROR)
            return make_response(message, 400)

        if command_name in KNOWN_COMMANDS_NAMES:
            message, message_status = KNOWN_COMMANDS[command_name](
                text, channel["id"]
            ).exec()
            webhook_send_message(webhook, message, message_status)
            return make_response("", 200)

        try:
            command = Command.find_one_by_name_and_chanel(command_name, channel["id"])
        except Command.DoesNotExist:
            message = f"No command found for {command_name}."
            webhook_send_message(webhook, message, MessageStatus.LIGHT_ERROR)
            return make_response(message, 400)

        message = CustomCommand(
            name=command.name,
            label=command.label,
            pick_list=command.pick_list,
            self_exclude=command.self_exclude,
        ).exec(user, text)
        webhook_send_message(webhook, message, MessageStatus.INFO)
        return make_response("", 200)

    except ArgError as error:
        return error_handler(error, webhook, 400)
    except Exception as error:
        return error_handler(error, webhook, 500)

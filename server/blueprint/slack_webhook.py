from flask import Blueprint

from server.blueprint.back_error import BackError
from server.command.custom import CustomCommand
from server.command.help import KNOWN_COMMANDS, KNOWN_COMMANDS_NAMES
from server.orm.command import Command
from server.slack.message_status import MessageStatus, MessageVisibility
from server.blueprint.decorators import format_body, send_return, validate, handle_error
from server.blueprint.slack_webhook_validator import SlackWebhookSchema

slack_webhook = Blueprint("slack_webhook", __name__, url_prefix="/slack_webhook")


@slack_webhook.route("/", methods=["POST"])
@handle_error
@format_body
@validate(SlackWebhookSchema)
@send_return
def slack_app(*, channel, user, command_name, text, **kwargs):
    if command_name in KNOWN_COMMANDS_NAMES:
        return KNOWN_COMMANDS[command_name](text, channel["id"]).exec(user["id"])

    try:
        command = Command.find_one_by_name_and_chanel(command_name, channel["id"])
    except Command.DoesNotExist:
        message = f"No command found for {command_name}."
        raise BackError(message, 400)

    message = CustomCommand(
        name=command.name,
        label=command.label,
        pick_list=command.pick_list,
        self_exclude=command.self_exclude,
    ).exec(user, text)

    return message, MessageStatus.INFO, MessageVisibility.NORMAL

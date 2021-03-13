import threading

from flask import Blueprint, current_app, make_response, request

from server.blueprint.decorators import (format_body, handle_error, make_context,
                                         send_to_channel, validate, validate_signature)
from server.blueprint.slack_webhook_validator import SlackWebhookSchema
from server.command.custom import CustomCommand
from server.command.help import KNOWN_COMMANDS, KNOWN_COMMANDS_NAMES
from server.orm.command import Command
from server.slack.message_status import MessageStatus, MessageVisibility

slack_webhook = Blueprint("slack_webhook", __name__, url_prefix="/slack_webhook")


@slack_webhook.route("/", methods=["POST"])
@validate_signature
@format_body
def slack_app(*args, **kwargs):

    thread = threading.Thread(
        target=resolve_command,
        args=(current_app._get_current_object(), *args),
        kwargs=kwargs,
    )
    thread.start()
    if current_app.config["WAIT_FOR_THREAD_BEFORE_RETURN"]:
        thread.join()

    command = f"{current_app.config['SLASH_COMMAND']} {request.form.get('text')}"
    return make_response(command, 200)


@make_context
@handle_error
@validate(SlackWebhookSchema)
@send_to_channel
def resolve_command(*, channel, user, command_name, text, **kwargs):
    # Known commands
    if command_name in KNOWN_COMMANDS_NAMES:
        return KNOWN_COMMANDS[command_name](text, channel["id"]).exec(user["id"])

    # Custom commands
    command = Command.find_one_by_name_and_chanel(command_name, channel["id"])
    message = CustomCommand(
        name=command.name,
        label=command.label,
        pick_list=command.pick_list,
        self_exclude=command.self_exclude,
    ).exec(user, text)

    return message, MessageStatus.INFO, MessageVisibility.NORMAL

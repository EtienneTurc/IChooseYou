import os
import threading

from flask import Blueprint, current_app, make_response, request
from slack_sdk import WebClient

from server.blueprint.decorators import (format_body, handle_error, make_context,
                                         send_to_channel, validate, validate_signature)
from server.blueprint.slack_api_validator import SlackApiSchema
from server.command.custom import CustomCommand
from server.command.help import KNOWN_COMMANDS, KNOWN_COMMANDS_NAMES
from server.orm.command import Command
from server.orm.slack_bot_token import SlackBotToken
from server.slack.message_status import MessageStatus, MessageVisibility

slack_api = Blueprint("api", __name__, url_prefix="/api/slack")

client_id = os.environ.get("SLACK_CLIENT_ID")
client_secret = os.environ.get("SLACK_CLIENT_SECRET")


@slack_api.route("/oauth_redirect", methods=["GET"])
def post_install():
    code_param = request.args["code"]

    client = WebClient()

    try:
        response = client.oauth_v2_access(
            client_id=client_id, client_secret=client_secret, code=code_param
        )

        SlackBotToken.create(
            team_id=response["team"]["id"],
            team_name=response["team"]["name"],
            scope=response["scope"],
            token_type=response["token_type"],
            access_token=response["access_token"],
            bot_user_id=response["bot_user_id"],
        )
    except Exception as e:
        return str(e)

    return "I choose you successfully installed!"


@slack_api.route("/", methods=["POST"])
@validate_signature
@format_body
def slash_command(*args, **kwargs):
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
@validate(SlackApiSchema)
@send_to_channel
def resolve_command(*, team_id, channel, user, command_name, text, **kwargs):
    # Known commands
    if command_name in KNOWN_COMMANDS_NAMES:
        return KNOWN_COMMANDS[command_name](
            text=text, team_id=team_id, channel_id=channel["id"]
        ).exec(user["id"])

    # Custom commands
    command = Command.find_one_by_name_and_chanel(command_name, channel["id"])
    message = CustomCommand(
        name=command.name,
        label=command.label,
        pick_list=command.pick_list,
        self_exclude=command.self_exclude,
    ).exec(user, text)

    return message, MessageStatus.INFO, MessageVisibility.NORMAL

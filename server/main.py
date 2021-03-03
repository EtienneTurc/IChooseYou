import os

from flask import Flask, make_response, request
from pymodm import connect
from slack_sdk.webhook import WebhookClient

from server.command.help import KNOWN_COMMANDS, KNOWN_COMMANDS_NAMES
from server.command.custom import CustomCommand
from server.orm.command import Command
from server.slack.utils import (
    error_handler,
    format_slack_request,
)
from server.slack.validator import check_incoming_request_is_valid

app = Flask(__name__)
connect(os.environ["DATABASE_URI"])


@app.route("/", methods=["POST"])
def slack_app():
    check_incoming_request_is_valid(request)
    channel, user, command_name, text, response_url = format_slack_request(request)
    webhook = WebhookClient(response_url)

    try:
        if not command_name:
            return make_response("I choose you request a command to be used", 400)

        if command_name in KNOWN_COMMANDS_NAMES:
            message = KNOWN_COMMANDS[command_name](text, channel.id).exec()
            webhook.send(
                text="",
                response_type="in_channel",
                replace_original=True,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{message}",
                        },
                    }
                ],
            )
            return make_response("", 200)

        command = Command.find_one_by_name_and_chanel(command_name, channel.id)
        if not command:
            return make_response(f"No command found for {command_name}", 400)

        message = CustomCommand(
            name=command.name,
            label=command.label,
            pick_list=command.pick_list,
            self_exclude=command.self_exclude,
        ).exec(user, text)

        webhook.send(
            text=f"{message}", response_type="in_channel", replace_original=True
        )
        return make_response("", 200)
    except Exception as error:
        return error_handler(error, webhook)

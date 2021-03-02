import os

from flask import Flask, make_response, request
from pymodm import connect
from slack_sdk.webhook import WebhookClient

from server.command import KNOWN_COMMANDS, CreateCommand, CustomCommand
from server.orm import Command
from server.slack import (check_incoming_request_is_valid, error_handler,
                          format_slack_request)

app = Flask(__name__)
connect(os.environ["DATABASE_URI"])


@app.route("/", methods=["POST"])
def slack_app():
    check_incoming_request_is_valid(request)
    user, command_name, text, response_url = format_slack_request(request)
    webhook = WebhookClient(response_url)

    try:
        if not command_name:
            return make_response("I choose you request a command to be used", 400)

        if command_name in KNOWN_COMMANDS:
            CreateCommand().exec(text)
            return make_response("", 200)

        command = Command.find_one_by_name(command_name)
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

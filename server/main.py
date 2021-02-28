import os

from flask import Flask, make_response, request
from pymodm import connect
from slack_sdk.webhook import WebhookClient
from .orm import Command
from .command import CreateCommand, CustomCommand, KNOWN_COMMANDS
from .utils import check_incoming_request_is_valid

app = Flask(__name__)
connect(os.environ["DATABASE_URI"])


@app.route("/", methods=["POST"])
def slack_app():
    check_incoming_request_is_valid(request)

    # channel = {
    #     "id": request.form.get("channel_id"),
    #     "name": request.form.get("channel_name"),
    # }
    user = {"id": request.form.get("user_id"), "name": request.form.get("user_name")}
    command_name = request.form.get("command")
    text = request.form.get("text")
    response_url = request.form.get("response_url")

    if not command_name:
        return make_response("I choose you request a command to be used", 400)

    if command_name in KNOWN_COMMANDS:
        CreateCommand().exec(text)
        return

    command = Command.find_one_by_name(command_name)
    if not command:
        return make_response(f"No command found for {command_name}", 400)
    message = CustomCommand(
        name=command.name,
        label=command.label,
        pick_list=command.pick_list,
        self_exclude=command.self_exclude,
    ).exec(user, text)

    webhook = WebhookClient(response_url)
    webhook.send(text=f"{message}")

    return make_response("", 200)

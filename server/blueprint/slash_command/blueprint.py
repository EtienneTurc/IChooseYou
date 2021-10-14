from flask import Blueprint, make_response, request

from server.blueprint.slash_command.action import (
    KNOWN_SLASH_COMMANDS_ACTIONS,
    BlueprintSlashCommandAction,
)
from server.service.formatter.slash_command import extract_command_from_text
from server.service.slack.decorator import validate_signature
from server.service.tpr.main import transform_process_respond

api = Blueprint("slash_command", __name__, url_prefix="/slash_command")


@api.route("/", methods=["POST"])
@validate_signature
def process_slash_command():
    command_name, _ = extract_command_from_text(request.form.get("text"))

    if command_name == "" or command_name is None:
        response = transform_process_respond(
            BlueprintSlashCommandAction.OPEN_MAIN_MODAl.value, request.form
        )

    elif command_name in KNOWN_SLASH_COMMANDS_ACTIONS:
        response = transform_process_respond(
            BlueprintSlashCommandAction[command_name.upper()].value,
            request.form,
        )
    else:
        response = transform_process_respond(
            BlueprintSlashCommandAction.CUSTOM.value,
            request.form,
        )
    return make_response(response, 200)

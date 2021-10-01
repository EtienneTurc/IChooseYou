import json

from flask import Blueprint, make_response, request

from server.service.slack.decorator import validate_signature
from server.service.formatter.interactivity import extract_interactivity_actions
from server.blueprint.interactivity.action import BlueprintInteractivityAction
from server.service.tpr.main import transform_process_respond
from server.service.slack.modal.enum import SlackModalAction

api = Blueprint("interactivity", __name__, url_prefix="/interactivity")

slack_modal_actions = [action.value for action in SlackModalAction]


@api.route("/", methods=["POST"])
@validate_signature
def proccess_interactivity():
    payload = json.loads(request.form.get("payload"))
    response = proccess_interactivity_for_response(payload)
    return make_response(response, 200)


def proccess_interactivity_for_response(payload: dict[str, any]) -> str:
    actions, callback_action = extract_interactivity_actions(payload)

    if callback_action in slack_modal_actions:
        return transform_process_respond(callback_action, payload)

    for action in BlueprintInteractivityAction:
        if action.value in actions:
            return transform_process_respond(action.value, payload)

    return "Action not handled"  # TODO

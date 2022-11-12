import json

from flask import Blueprint, make_response, request

from server.blueprint.interactivity.action import (BlueprintInteractivityAction,
                                                   BlueprintInteractivityBlockAction)
from server.service.formatter.interactivity import extract_interactivity_actions
from server.service.slack.decorator import validate_signature
from server.service.slack.modal.enum import SlackModalSubmitAction
from server.service.slack.modal.instant_command_modal import \
    SlackInstantCommandModalActionId
from server.service.slack.modal.upsert_command_modal import \
    SlackUpsertCommandModalActionId
from server.service.tpr.main import transform_process_respond

api = Blueprint("interactivity", __name__, url_prefix="/interactivity")

slack_modal_actions = [action.value for action in SlackModalSubmitAction]

slack_modal_actions_to_ignore = [
    SlackUpsertCommandModalActionId.SELF_EXCLUDE_CHECKBOX,
    SlackUpsertCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX,
    SlackInstantCommandModalActionId.ONLY_ACTIVE_USERS_CHECKBOX,
    SlackInstantCommandModalActionId.WITH_WHEEL_CHECKBOX,
]


@api.route("/", methods=["POST"])
@validate_signature
def proccess_interactivity():
    payload = json.loads(request.form.get("payload"))
    response = proccess_interactivity_for_response(payload)
    return make_response(response, 200)


def proccess_interactivity_for_response(payload: dict[str, any]) -> str:
    actions, callback_action = extract_interactivity_actions(payload)

    for action in slack_modal_actions_to_ignore:
        if action.value in actions:
            return "Action ignored"

    if "block_actions" in actions:
        for action in BlueprintInteractivityBlockAction:
            if action.value in actions:
                return transform_process_respond(
                    blueprint_action=action.value, request_payload=payload
                )

    if callback_action in slack_modal_actions:
        return transform_process_respond(
            blueprint_action=callback_action, request_payload=payload
        )

    for action in BlueprintInteractivityAction:
        if action.value in actions:
            return transform_process_respond(
                blueprint_action=action.value, request_payload=payload
            )

    return "Action not handled"

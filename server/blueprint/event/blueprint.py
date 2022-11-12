import json

from flask import Blueprint, make_response, request

from server.blueprint.event.action import BlueprintEventAction
from server.service.helper.dict_helper import get_by_path
from server.service.slack.decorator import validate_challenge
from server.service.tpr.main import transform_process_respond

api = Blueprint("event", __name__, url_prefix="/event")


@api.route("/", methods=["POST"])
@validate_challenge
def proccess_event():
    payload = json.loads(request.get_data())
    response = process_event_for_response(payload)
    return make_response(response, 200)


def process_event_for_response(payload: dict[str, any]) -> str:
    event_types = [get_by_path(payload, "event.type")]

    for action in BlueprintEventAction:
        if action.value in event_types:
            transform_process_respond(
                blueprint_action=action.value, request_payload=payload
            )

    return "Event not handled"

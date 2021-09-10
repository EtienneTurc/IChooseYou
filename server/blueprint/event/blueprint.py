import json

from flask import Blueprint, make_response, request

import server.blueprint.event.service as service
from server.service.slack.decorator import validate_challenge

api = Blueprint("event", __name__, url_prefix="/event")


@api.route("/", methods=["POST"])
@validate_challenge
def proccess_event():
    payload = json.loads(request.get_data())
    response = service.process_event(payload)
    return make_response(response, 200)

import json

from flask import Blueprint, make_response, request

import server.blueprint.interactivity.service as service
from server.service.slack.decorator import validate_signature

api = Blueprint("interactivity", __name__, url_prefix="/interactivity")


@validate_signature
@api.route("/", methods=["POST"])
def proccess_interactivity():
    payload = json.loads(request.form.get("payload"))
    response = service.proccess_interactivity(payload)
    return make_response(response, 200)

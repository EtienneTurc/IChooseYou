from flask import Blueprint, make_response, request

import server.blueprint.slash_command.service as service
from server.blueprint.slash_command.helper import format_body
from server.service.slack.decorator import validate_signature

api = Blueprint("slash_command", __name__, url_prefix="/slash_command")


@api.route("/", methods=["POST"])
@validate_signature
def process_slash_command():
    body = format_body(request.form)
    response = service.process_slash_command(body)
    return make_response(response, 200)

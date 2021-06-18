import os

from flask import Blueprint, request

import server.blueprint.authentication.service as service

api = Blueprint("authentication", __name__, url_prefix="/authentication")

client_id = os.environ.get("SLACK_CLIENT_ID")
client_secret = os.environ.get("SLACK_CLIENT_SECRET")


@api.route("/register", methods=["GET"])
def register():
    code = request.args["code"]
    return service.register(code)

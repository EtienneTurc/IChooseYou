from flask import Blueprint, request, send_file

import server.blueprint.chart.service as service

api = Blueprint("chart", __name__, url_prefix="/chart")


@api.route("/heat-map", methods=["GET"])
def show_heat_map():
    command_name = request.args.get("command_name")
    channel_id = request.args.get("channel_id")
    file, mimetype = service.create_heat_map(command_name, channel_id)
    return send_file(file, mimetype=mimetype)

from flask import Blueprint, request, send_file

# import numpy as np
import server.blueprint.chart.service as service

# from matplotlib.figure import Figure


api = Blueprint("chart", __name__, url_prefix="/chart")


@api.route("/heat-map", methods=["GET"])
def show_heat_map():
    command_name = request.args.get("command_name")
    channel_id = request.args.get("channel_id")
    file, mimetype = service.create_heat_map(command_name, channel_id)
    return send_file(file, mimetype=mimetype)


# @api.route("/bar", methods=["GET"])
# def show_bar_chart():
#     # Make a random dataset:
#     height = [3, 12, 5, 18, 45]
#     bars = ("A", "B", "C", "D", "E")
#     y_pos = np.arange(len(bars))

#     fig = Figure()
#     ax = fig.subplots()

#     # Create bars
#     ax.bar(y_pos, height)

#     # Create names on the x-axis
#     ax.set_xticks(y_pos)
#     ax.set_xticklabels(bars)

#     ax.set_yticks([10, 20, 30, 40, 100])
#     ax.set_yticklabels(bars)

#     buf = io.BytesIO()
#     fig.savefig(buf, format="png")
#     buf.seek(0)
#     return send_file(buf, mimetype="image/png")

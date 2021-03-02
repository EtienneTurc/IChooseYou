from flask import make_response


def format_slack_request(request):
    # channel = {
    #     "id": request.form.get("channel_id"),
    #     "name": request.form.get("channel_name"),
    # }
    user = {"id": request.form.get("user_id"), "name": request.form.get("user_name")}
    text = request.form.get("text")
    command_name = text.split(" ")[0]
    text = " ".join(text.split(" ")[1:])
    response_url = request.form.get("response_url")

    return [user, command_name, text, response_url]


def error_handler(error, webhook):
    webhook.send(text=f"{error}")
    return make_response(f"{error}", 500)

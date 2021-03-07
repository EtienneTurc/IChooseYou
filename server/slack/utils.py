import traceback

from flask import make_response

from server.slack.message_status import MessageStatus


def format_slack_request(request):
    channel = {
        "id": request.form.get("channel_id"),
        "name": request.form.get("channel_name"),
    }
    user = {"id": request.form.get("user_id"), "name": request.form.get("user_name")}
    text = request.form.get("text")
    command_name = text.split(" ")[0]
    text = " ".join(text.split(" ")[1:])
    response_url = request.form.get("response_url")

    return [channel, user, command_name, text, response_url]


def error_handler(error, webhook, status_code):
    webhook_send_message(
        webhook,
        f"{error}",
        MessageStatus.LIGHT_ERROR if status_code == 400 else MessageStatus.ERROR,
    )
    print(error)
    traceback.print_exc()
    return make_response(f"{error}", status_code)


def webhook_send_message(webhook, message, message_status=None):
    webhook.send(
        text="",
        response_type="in_channel",
        replace_original=True,
        attachments=[
            {
                "color": message_status.value if message_status else MessageStatus.INFO,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{message}",
                        },
                    }
                ],
            }
        ],
    )

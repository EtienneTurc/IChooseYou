from server.blueprint.slash_command.service import process_slash_command


def proccess_interactivity(payload):
    callback_id = payload.get("callback_id")
    if callback_id == "tender_button":
        body = {
            "text": "help test_mention",
            "channel_id": payload.get("channel").get("id"),
            "channel_name": payload.get("channel").get("name"),
            "user_id": payload.get("user").get("id"),
            "user_name": payload.get("user").get("name"),
            "response_url": payload.get("response_url"),
            "team_id": payload.get("team").get("id"),
        }
        return process_slash_command(body)
    return "Action not handled"

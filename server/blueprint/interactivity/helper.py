def format_payload_for_slash_command(payload):
    text = payload.get("actions")[0].get("value")
    command_name = text.split(" ")[0]
    text = " ".join(text.split(" ")[1:])
    return {
        "channel": {
            "id": payload.get("channel").get("id"),
            "name": payload.get("channel").get("name"),
        },
        "user": {
            "id": payload.get("user").get("id"),
            "name": payload.get("user").get("name"),
        },
        "response_url": payload.get("response_url"),
        "team_id": payload.get("team").get("id"),
        "text": text,
        "command_name": command_name,
    }

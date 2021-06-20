def format_body(form):
    text = form.get("text")
    command_name = text.split(" ")[0]
    text = " ".join(text.split(" ")[1:])
    return {
        "channel": {
            "id": form.get("channel_id"),
            "name": form.get("channel_name"),
        },
        "user": {
            "id": form.get("user_id"),
            "name": form.get("user_name"),
        },
        "response_url": form.get("response_url"),
        "team_id": form.get("team_id"),
        "text": text,
        "command_name": command_name,
    }

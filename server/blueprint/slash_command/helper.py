def extract_command_from_text(text):
    separator = " "
    text = text.replace("\n", f"{separator}\n")
    command_name = text.split(separator)[0]
    return command_name, separator.join(text.split(separator)[1:])


def format_body(form):
    command_name, text = extract_command_from_text(form.get("text"))
    return {
        "channel_id": form.get("channel_id"),
        "user": {
            "id": form.get("user_id"),
            "name": form.get("user_name"),
        },
        "response_url": form.get("response_url"),
        "team_id": form.get("team_id"),
        "text": text,
        "trigger_id": form.get("trigger_id"),
        "command_name": command_name,
    }

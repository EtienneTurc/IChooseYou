from server.blueprint.slash_command.helper import extract_command_from_text
from server.service.error.back_error import BackError


def format_payload_for_slash_command(payload):
    command_name, text = extract_command_from_text(
        payload.get("actions")[0].get("value")
    )
    return {
        "channel": {
            "id": payload.get("channel").get("id"),
            "name": payload.get("channel").get("name"),
        },
        "user": {
            "id": payload.get("user").get("id"),
            "name": payload.get("user").get("name"),
        },
        "team_id": payload.get("team").get("id"),
        "text": text,
        "command_name": command_name,
        "response_url": payload.get("response_url"),
    }


def format_payload_for_message_delete(payload):
    return {
        "channel_id": payload.get("channel").get("id"),
        "user_id": payload.get("user").get("id"),
        "team_id": payload.get("team").get("id"),
        "text": payload.get("message").get("text"),
        "ts": payload.get("message").get("ts"),
        "response_url": payload.get("response_url"),
    }


def assert_message_can_be_delete(text: str, user_id: str) -> bool:
    text_split = text.split("Hey ! <@")
    if len(text_split) <= 1:
        raise BackError("Only pick messages can be deleted.", 400)

    user_id_size = len(user_id)
    expected_user_id = text_split[1][:user_id_size]

    if expected_user_id != user_id:
        message = "Only the user that triggered the slash command can delete"
        message += " the corresponding message."
        raise BackError(message, 400)

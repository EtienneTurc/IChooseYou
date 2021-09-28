from server.service.command_line.formatter import parse_command_line
from server.service.command_line.arg import Arg


def extract_command_from_text(text):
    separator = " "
    text = text.replace("\n", f"{separator}\n")
    command_name = text.split(separator)[0]
    return command_name, separator.join(text.split(separator)[1:])


def format_slash_command_payload(
    payload: dict[str, any],
    *,
    expected_positional_args: list[Arg],
    expected_named_args: list[Arg],
):
    command_name, text = extract_command_from_text(payload.get("text"))

    return {
        **parse_command_line(text, expected_positional_args, expected_named_args),
        "channel_id": payload.get("channel_id"),
        "user_id": payload.get("user_id"),
        "response_url": payload.get("response_url"),
        "team_id": payload.get("team_id"),
        "trigger_id": payload.get("trigger_id"),
        "command_name": command_name,
    }

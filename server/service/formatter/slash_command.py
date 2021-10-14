from server.service.command_line.arg import Arg
from server.service.command_line.formatter import parse_command_line


def extract_command_from_text(text: str) -> tuple[str, str]:
    separator = " "
    text = text.replace("\n", f"{separator}\n")
    command_name = text.split(separator)[0]
    return command_name, separator.join(text.split(separator)[1:])


def format_slash_command_basic_payload(payload: dict[str, any]) -> dict[str, any]:
    return {
        "channel_id": payload.get("channel_id"),
        "user_id": payload.get("user_id"),
        "response_url": payload.get("response_url"),
        "team_id": payload.get("team_id"),
        "trigger_id": payload.get("trigger_id"),
    }


def format_slash_command_payload(
    payload: dict[str, any],
    *,
    expected_positional_args: list[Arg],
    expected_named_args: list[Arg],
    **kwargs,
) -> dict[str, any]:
    command_name, text = extract_command_from_text(payload.get("text"))

    return {
        **parse_command_line(text, expected_positional_args, expected_named_args),
        **format_slash_command_basic_payload(payload),
        "command_name": command_name,
        **kwargs,
    }

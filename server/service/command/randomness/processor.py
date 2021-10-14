from datetime import datetime

from flask import current_app

from server.orm.command import Command
from server.service.command.randomness.schema import RandomnessCommandProcessorSchema
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.validator.decorator import validate_schema


@validate_schema(RandomnessCommandProcessorSchema)
def randomness_command_processor(
    *,
    channel_id: str,
    command_to_show_randomness: str,
) -> dict[str, any]:
    Command.find_one_by_name_and_chanel(
        command_to_show_randomness, channel_id=channel_id
    )

    api_url = current_app.config["API_URL"]
    params = {
        "command_name": command_to_show_randomness,
        "channel_id": channel_id,
        "t": datetime.now().timestamp(),
    }
    image_url = construct_url(f"{api_url}/chart/heat-map", params)
    message = "*Randomness of the command*\n"
    message += "Each color represents a different item of the pick list"

    return {
        "message": Message(
            content=message,
            status=MessageStatus.INFO,
            visibility=MessageVisibility.HIDDEN,
            as_attachment=True,
            image_url=image_url,
        )
    }


def construct_url(base_url: str, params: dict[str, str]) -> str:
    params_url = ""
    for param_key in params:
        params_url += f"&{param_key}={params[param_key]}"

    if params_url:
        params_url = f"?{params_url[1:]}"

    return base_url + params_url

from datetime import datetime

from flask import current_app

from server.orm.command import Command
from server.service.command.args import Arg
from server.service.command.base_command import BaseCommand, addHelp
from server.service.slack.message import Message, MessageStatus, MessageVisibility


def construct_url(base_url: str, params: dict[str, str]) -> str:
    params_url = ""
    for param_key in params:
        params_url += f"&{param_key}={params[param_key]}"

    if params_url:
        params_url = f"?{params_url[1:]}"

    return base_url + params_url


class RandomnessCommand(BaseCommand):
    def __init__(self, *, text: str, team_id: str, channel_id: str):
        name = "randomness"
        description = "Visualize the randomness of the given command"
        examples = [
            "my_command_to_visualize_randomness",
        ]
        args = [
            Arg(
                name="command_name",
                prefix="",
                nargs=1,
                help="Name of the command to visualize randomness.",
            ),
        ]
        super(RandomnessCommand, self).__init__(
            text,
            name=name,
            channel_id=channel_id,
            team_id=team_id,
            description=description,
            examples=examples,
            args=args,
        )

    @addHelp
    def exec(self, *args, **kwargs):
        command_name = self.options.get("command_name")
        Command.find_one_by_name_and_chanel(command_name, channel_id=self.channel_id)

        api_url = current_app.config["API_URL"]
        params = {
            "command_name": command_name,
            "channel_id": self.channel_id,
            "t": datetime.now().timestamp(),
        }
        image_url = construct_url(f"{api_url}/chart/heat-map", params)
        message = "*Randomness of the command*\n"
        message += "Each color represents a different item of the pick list"
        return Message(
            content=message,
            status=MessageStatus.INFO,
            visibility=MessageVisibility.HIDDEN,
            as_attachment=True,
            image_url=image_url,
        )

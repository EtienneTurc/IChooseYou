from flask import current_app

from server.service.command.args import Arg
from server.service.command.base_command import BaseCommand, addHelp
from server.service.slack.message import Message, MessageStatus, MessageVisibility


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

        api_url = current_app.config["API_URL"]
        image_url = f"{api_url}/chart/heat-map?command_name={command_name}&channel_id={self.channel_id}"  # noqa E501
        message = "*Randomness of the command*\n"
        message += "Each color represents a different item of the pick list"
        return Message(
            content=message,
            status=MessageStatus.INFO,
            visibility=MessageVisibility.HIDDEN,
            as_attachment=True,
            image_url=image_url,
        )

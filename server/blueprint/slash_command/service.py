import threading

from flask import current_app

from server.blueprint.slash_command.schema import SlackApiSchema
from server.orm.command import Command
from server.service.command.custom import CustomCommand
from server.service.command.help import KNOWN_COMMANDS, KNOWN_COMMANDS_NAMES
from server.service.error.decorator import handle_error
from server.service.flask.decorator import make_context
from server.service.slack.response import send_to_channel
from server.service.validator.decorator import validate_schema


def process_slash_command(body):
    thread = threading.Thread(
        target=resolve_command,
        args=(current_app._get_current_object(),),
        kwargs=body,
    )
    thread.start()
    if current_app.config["WAIT_FOR_THREAD_BEFORE_RETURN"]:
        thread.join()

    button = [
        {
            "text": f"{current_app.config['SLASH_COMMAND']} "
            + f"{body.get('command_name')} {body.get('text')}"
        },
        {
            "callback_id": "tender_button",
            "attachment_type": "default",
            "actions": [
                {"name": "press", "text": "Press", "type": "button", "value": "pressed"}
            ],
        },
    ]

    return {"attachments": button}


@make_context
@handle_error
@validate_schema(SlackApiSchema)
def resolve_command(
    *, team_id, channel, user, command_name, text, response_url, **kwargs
):
    # Known commands
    if command_name in KNOWN_COMMANDS_NAMES:
        message = KNOWN_COMMANDS[command_name](
            text=text, team_id=team_id, channel_id=channel["id"]
        ).exec(user["id"])

    # Custom commands
    else:
        command = Command.find_one_by_name_and_chanel(command_name, channel["id"])
        message = CustomCommand(
            name=command.name,
            label=command.label,
            pick_list=command.pick_list,
            self_exclude=command.self_exclude,
        ).exec(user, text)

    return send_to_channel(message, response_url)

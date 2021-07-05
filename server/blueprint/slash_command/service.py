from flask import current_app

from server.blueprint.interactivity.action import Action
from server.blueprint.slash_command.schema import SlackApiSchema
from server.orm.command import Command
from server.service.command.custom import CustomCommand
from server.service.command.help import KNOWN_COMMANDS, KNOWN_COMMANDS_NAMES
from server.service.error.decorator import handle_error
from server.service.flask.decorator import make_context
from server.service.helper.thread import launch_function_in_thread
from server.service.slack.message import Message
from server.service.slack.sdk_wrapper import send_message_to_channel
from server.service.strategy.helper import get_strategy
from server.service.validator.decorator import validate_schema


def process_slash_command(body):
    launch_function_in_thread(resolve_command_and_send_to_slack, body)

    slash_command = f"{current_app.config['SLASH_COMMAND']} "
    command = f"{body.get('command_name')} {body.get('text')}"
    return {
        "attachments": [
            {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": slash_command + command,
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Resubmit command",
                                "emoji": True,
                            },
                            "value": command,
                            "action_id": Action.RESUBMIT_COMMAND.value,
                        },
                    }
                ]
            }
        ]
    }


@make_context
@handle_error
@validate_schema(SlackApiSchema)
def resolve_command_and_send_to_slack(
    *,
    team_id: str,
    channel: dict[str, str],
    user: dict[str, str],
    command_name: str,
    text: str,
    **kwargs,
):
    message, _ = resolve_command(
        team_id=team_id,
        channel=channel,
        user=user,
        command_name=command_name,
        text=text,
    )
    return send_message_to_channel(message, channel["id"], team_id, user_id=user["id"])


def resolve_command(
    *,
    team_id: str,
    channel: dict[str, str],
    user: dict[str, str],
    command_name: str,
    text: str,
) -> tuple[Message, str]:
    selected_items = None
    # Known commands
    if command_name in KNOWN_COMMANDS_NAMES:
        message = KNOWN_COMMANDS[command_name](
            text=text, team_id=team_id, channel_id=channel["id"]
        ).exec(user["id"])

    # Custom commands
    else:
        command = Command.find_one_by_name_and_chanel(command_name, channel["id"])
        message, selected_items = CustomCommand(
            name=command.name,
            label=command.label,
            pick_list=command.pick_list,
            weight_list=command.weight_list,
            strategy=command.strategy,
            self_exclude=command.self_exclude,
            only_active_users=command.only_active_users,
            text=text,
        ).exec(user["id"], team_id=team_id)

        # Update weight_list
        strategy = get_strategy(command.strategy, command.weight_list)
        strategy.update(
            indices_selected=[
                command.pick_list.index(selected_item)
                for selected_item in selected_items
            ]
        )
        Command.update(
            command.name,
            command.channel_id,
            command.updated_by_user_id,
            {"weight_list": strategy.weight_list},
        )

    return message, selected_items

from server.orm.command import Command
from server.service.slack.modal.main_modal import build_main_modal
from server.service.slack.modal.custom_command_modal import build_custom_command_modal
from server.service.tpr.response_format import Response
from server.service.slack.response.response_type import SlackResponseType


def open_main_modal_processor(
    *,
    channel_id: str,
    **kwargs,
) -> Response:
    commands = Command.find_all_in_chanel(channel_id)
    modal = build_main_modal(commands=commands, **kwargs)

    return Response(
        type=SlackResponseType.SLACK_OPEN_VIEW_MODAL.value,
        data={"modal": modal},
    )


def main_modal_select_command_processor(
    *,
    command_name: str,
    channel_id: str,
    **kwargs,
) -> Response:
    command = Command.find_one_by_name_and_chanel(command_name, channel_id)
    modal = build_custom_command_modal(
        command_id=command._id,
        command_name=command.name,
        size_of_pick_list=len(command.pick_list),
    )
    return Response(
        type=SlackResponseType.SLACK_PUSH_NEW_VIEW_MODAL.value,
        data={"modal": modal},
    )

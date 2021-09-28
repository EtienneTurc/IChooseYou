from server.orm.command import Command
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.tpr.response_format import Response
from server.service.slack.response.response_type import SlackResponseType


# @validate_payload TODO Use marshmallow schema instead
def delete_command_processor(
    *,
    channel_id: str,
    command_to_delete: str,
    **kwargs,
) -> Response:
    command = Command.find_one_by_name_and_chanel(command_to_delete, channel_id)
    Command.delete_command(command)

    message_content = f"Command {command_to_delete} successfully deleted."

    return Response(
        type=SlackResponseType.SLACK_SEND_MESSAGE_IN_CHANNEL.value,
        data={
            "message": Message(
                content=message_content,
                status=MessageStatus.INFO,
                visibility=MessageVisibility.NORMAL,
            )
        },
    )

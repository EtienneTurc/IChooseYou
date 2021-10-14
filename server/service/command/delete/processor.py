from server.orm.command import Command
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.validator.decorator import validate_schema
from server.service.command.delete.schema import DeleteCommandProcessorSchema


@validate_schema(DeleteCommandProcessorSchema)
def delete_command_processor(
    *,
    channel_id: str,
    command_to_delete: str,
) -> dict[str, any]:
    command = Command.find_one_by_name_and_chanel(command_to_delete, channel_id)
    Command.delete_command(command)

    message_content = f"Command {command_to_delete} successfully deleted."

    return {
        "message": Message(
            content=message_content,
            status=MessageStatus.INFO,
            visibility=MessageVisibility.NORMAL,
        )
    }

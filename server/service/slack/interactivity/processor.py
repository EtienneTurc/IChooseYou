from server.service.command.custom.processor import custom_command_processor
from server.service.slack.interactivity.helper import assert_message_can_be_delete
from server.service.slack.interactivity.schema import DeleteMessageProcessorSchema
from server.service.slack.response.api_response import (delete_file_message,
                                                        delete_message_in_channel)
from server.service.validator.decorator import validate_schema


@validate_schema(DeleteMessageProcessorSchema)
def delete_message_processor(
    *, user_id: str, channel_id: str, team_id: str, message_text: str, ts: str, **kwargs
) -> dict[str, any]:
    if message_text:
        assert_message_can_be_delete(message_text, user_id)

    delete_message_in_channel(channel_id=channel_id, ts=ts, team_id=team_id)
    return {}


def resubmit_command_and_delete_message_processor(
    file_id: str = None, *, ts: str, **kwargs
) -> dict[str, any]:
    delete_message_processor(ts=ts, **kwargs)
    if file_id:
        delete_file_message(file_id=file_id, **kwargs)

    return custom_command_processor(**kwargs, should_update_command=True)

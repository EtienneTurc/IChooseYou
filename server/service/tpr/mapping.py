from server.blueprint.slash_command.action import BlueprintSlashCommandAction
from server.service.command.create.processor import create_command_processor
from server.service.command.create.command_line_args import (
    POSITIONAL_ARG as CREATE_POSITIONAL_ARGS,
    NAMED_ARGS as CREATE_NAMED_ARGS,
)
from server.service.formatter.slash_command import format_slash_command_payload
from dataclasses import dataclass
import functools
from server.service.slack.response.response_type import SlackResponseType
from server.service.slack.response.api_response import (
    send_message_to_channel,
    delete_message_in_channel,
    send_message_to_channel_via_response_url,
    open_view_modal,
    push_new_view_modal,
    save_workflow,
    complete_workflow,
    failed_worklow,
)


@dataclass
class DataFlow:
    formatter: any
    processor: any  # Need a validator


BLUEPRINT_ACTION_TO_DATA_FLOW = {
    BlueprintSlashCommandAction.CREATE.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=CREATE_POSITIONAL_ARGS,
            expected_named_args=CREATE_NAMED_ARGS,
        ),
        processor=create_command_processor,
    )
}


RESPONSE_TYPE_TO_RESPONSE_ACTION = {
    SlackResponseType.SLACK_SEND_MESSAGE_IN_CHANNEL.value: send_message_to_channel,
    SlackResponseType.SLACK_DELETE_MESSAGE_IN_CHANNEL.value: delete_message_in_channel,
    SlackResponseType.SLACK_SEND_MESSAGE_IN_CHANNEL_VIA_WEBHOOK.value: send_message_to_channel_via_response_url,  # noqa E501
    SlackResponseType.SLACK_OPEN_VIEW_MODAL.value: open_view_modal,
    SlackResponseType.SLACK_PUSH_NEW_VIEW_MODAL.value: push_new_view_modal,
    SlackResponseType.SLACK_SAVE_WORKFLOW.value: save_workflow,
    SlackResponseType.SLACK_COMPLETE_WORKFLOW.value: complete_workflow,
    SlackResponseType.SLACK_FAILED_WORKFLOW.value: failed_worklow,
}

from server.blueprint.slash_command.action import BlueprintSlashCommandAction
from server.service.command.create.processor import create_command_processor
from server.service.command.create.command_line_args import (
    POSITIONAL_ARG as CREATE_POSITIONAL_ARGS,
    NAMED_ARGS as CREATE_NAMED_ARGS,
)
from server.service.command.update.processor import update_command_processor
from server.service.command.update.command_line_args import (
    POSITIONAL_ARG as UPDATE_POSITIONAL_ARGS,
    NAMED_ARGS as UPDATE_NAMED_ARGS,
)
from server.service.command.delete.processor import delete_command_processor
from server.service.command.delete.command_line_args import (
    POSITIONAL_ARG as DELETE_POSITIONAL_ARGS,
    NAMED_ARGS as DELETE_NAMED_ARGS,
)
from server.service.command.randomness.processor import randomness_command_processor
from server.service.command.randomness.command_line_args import (
    POSITIONAL_ARG as RANDOMNESS_POSITIONAL_ARGS,
    NAMED_ARGS as RANDOMNESS_NAMED_ARGS,
)
from server.service.command.custom.processor import custom_command_processor
from server.service.command.custom.command_line_args import (
    POSITIONAL_ARG as CUSTOM_POSITIONAL_ARGS,
    NAMED_ARGS as CUSTOM_NAMED_ARGS,
)
from server.service.slack.modal.processor import open_main_modal_processor
from server.service.formatter.slash_command import (
    format_slash_command_basic_payload,
    format_slash_command_payload,
)
from server.service.formatter.interactivity import (
    format_interactivity_delete_message_payload,
    format_interactivity_edit_workflow_payload,
    format_interactivity_save_workflow_payload,
    format_main_modal_select_command_payload,
    format_run_custom_command_payload,
)
from server.service.slack.interactivity.processor import (
    delete_message_processor,
)
from server.service.slack.workflow.processor import (
    edit_workflow_processor,
    save_workflow_processor,
)
from server.service.slack.modal.processor import main_modal_select_command_processor
from server.blueprint.interactivity.action import BlueprintInteractivityAction

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
from server.service.slack.modal.enum import SlackModalAction


@dataclass
class DataFlow:
    formatter: any
    processor: any  # Need a validator


BLUEPRINT_ACTION_TO_DATA_FLOW = {
    # ----------------------------------------------------------
    # ------------------- SLASH COMMAND ------------------------
    # ----------------------------------------------------------
    BlueprintSlashCommandAction.CREATE.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=CREATE_POSITIONAL_ARGS,
            expected_named_args=CREATE_NAMED_ARGS,
        ),
        processor=create_command_processor,
    ),
    BlueprintSlashCommandAction.UPDATE.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=UPDATE_POSITIONAL_ARGS,
            expected_named_args=UPDATE_NAMED_ARGS,
        ),
        processor=update_command_processor,
    ),
    BlueprintSlashCommandAction.DELETE.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=DELETE_POSITIONAL_ARGS,
            expected_named_args=DELETE_NAMED_ARGS,
        ),
        processor=delete_command_processor,
    ),
    BlueprintSlashCommandAction.RANDOMNESS.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=RANDOMNESS_POSITIONAL_ARGS,
            expected_named_args=RANDOMNESS_NAMED_ARGS,
        ),
        processor=randomness_command_processor,
    ),
    BlueprintSlashCommandAction.CUSTOM.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=CUSTOM_POSITIONAL_ARGS,
            expected_named_args=CUSTOM_NAMED_ARGS,
            should_update_weight_list=True,
        ),
        processor=custom_command_processor,
    ),
    BlueprintSlashCommandAction.OPEN_MAIN_MODAl.value: DataFlow(
        formatter=format_slash_command_basic_payload,
        processor=open_main_modal_processor,
    ),
    # ----------------------------------------------------------
    # ------------------- INTERACTIVITY ------------------------
    # ----------------------------------------------------------
    BlueprintInteractivityAction.DELETE_MESSAGE.value: DataFlow(
        formatter=format_interactivity_delete_message_payload,
        processor=delete_message_processor,
    ),
    BlueprintInteractivityAction.EDIT_WORKFLOW.value: DataFlow(
        formatter=format_interactivity_edit_workflow_payload,
        processor=edit_workflow_processor,
    ),
    BlueprintInteractivityAction.VIEW_SUBMISSION.value: DataFlow(  # TODO save workflow with modal action? # noqa E501
        formatter=format_interactivity_save_workflow_payload,
        processor=save_workflow_processor,
    ),
    BlueprintInteractivityAction.MAIN_MODAL_SELECT_COMMAND.value: DataFlow(
        formatter=format_main_modal_select_command_payload,
        processor=main_modal_select_command_processor,
    ),
    SlackModalAction.RUN_CUSTOM_COMMAND.value: DataFlow(
        formatter=format_run_custom_command_payload, processor=custom_command_processor
    ),
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

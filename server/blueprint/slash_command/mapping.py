import functools

from server.blueprint.slash_command.action import BlueprintSlashCommandAction
from server.service.command.create.command_line_args import \
    NAMED_ARGS as CREATE_NAMED_ARGS
from server.service.command.create.command_line_args import \
    POSITIONAL_ARG as CREATE_POSITIONAL_ARGS
from server.service.command.create.processor import create_command_processor
from server.service.command.custom.command_line_args import \
    NAMED_ARGS as CUSTOM_NAMED_ARGS
from server.service.command.custom.command_line_args import \
    POSITIONAL_ARG as CUSTOM_POSITIONAL_ARGS
from server.service.command.custom.processor import custom_command_processor
from server.service.command.delete.command_line_args import \
    NAMED_ARGS as DELETE_NAMED_ARGS
from server.service.command.delete.command_line_args import \
    POSITIONAL_ARG as DELETE_POSITIONAL_ARGS
from server.service.command.delete.processor import delete_command_processor
from server.service.command.instant.command_line_args import \
    NAMED_ARGS as INSTANT_NAMED_ARGS
from server.service.command.instant.command_line_args import \
    POSITIONAL_ARG as INSTANT_POSITIONAL_ARGS
from server.service.command.instant.processor import instant_command_processor
from server.service.command.randomness.command_line_args import \
    NAMED_ARGS as RANDOMNESS_NAMED_ARGS
from server.service.command.randomness.command_line_args import \
    POSITIONAL_ARG as RANDOMNESS_POSITIONAL_ARGS
from server.service.command.randomness.processor import randomness_command_processor
from server.service.command.update.command_line_args import \
    NAMED_ARGS as UPDATE_NAMED_ARGS
from server.service.command.update.command_line_args import \
    POSITIONAL_ARG as UPDATE_POSITIONAL_ARGS
from server.service.command.update.processor import update_command_processor
from server.service.error.handler.generic import on_error_handled_send_message
from server.service.formatter.slash_command import (format_slash_command_basic_payload,
                                                    format_slash_command_payload)
from server.service.slack.modal.processor import open_main_modal_processor
from server.service.slack.responder.message import (
    send_message_and_gif_to_channel, send_message_and_gif_to_channel_with_resubmit_button)
from server.service.slack.response.api_response import (open_view_modal,
                                                        send_message_to_channel)
from server.service.tpr.enum import DataFlow

BLUEPRINT_SLASH_COMMAND_ACTION_TO_DATA_FLOW = {
    BlueprintSlashCommandAction.CREATE.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=CREATE_POSITIONAL_ARGS,
            expected_named_args=CREATE_NAMED_ARGS,
        ),
        processor=create_command_processor,
        responder=send_message_to_channel,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintSlashCommandAction.UPDATE.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=UPDATE_POSITIONAL_ARGS,
            expected_named_args=UPDATE_NAMED_ARGS,
        ),
        processor=update_command_processor,
        responder=send_message_to_channel,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintSlashCommandAction.DELETE.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=DELETE_POSITIONAL_ARGS,
            expected_named_args=DELETE_NAMED_ARGS,
        ),
        processor=delete_command_processor,
        responder=send_message_to_channel,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintSlashCommandAction.RANDOMNESS.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=RANDOMNESS_POSITIONAL_ARGS,
            expected_named_args=RANDOMNESS_NAMED_ARGS,
        ),
        processor=randomness_command_processor,
        responder=send_message_to_channel,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintSlashCommandAction.INSTANT.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=INSTANT_POSITIONAL_ARGS,
            expected_named_args=INSTANT_NAMED_ARGS,
        ),
        processor=instant_command_processor,
        responder=send_message_and_gif_to_channel,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintSlashCommandAction.CUSTOM.value: DataFlow(
        formatter=functools.partial(
            format_slash_command_payload,
            expected_positional_args=CUSTOM_POSITIONAL_ARGS,
            expected_named_args=CUSTOM_NAMED_ARGS,
        ),
        processor=functools.partial(
            custom_command_processor, should_update_weight_list=True
        ),
        responder=send_message_and_gif_to_channel_with_resubmit_button,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintSlashCommandAction.OPEN_MAIN_MODAl.value: DataFlow(
        formatter=format_slash_command_basic_payload,
        processor=open_main_modal_processor,
        responder=open_view_modal,
        error_handler=on_error_handled_send_message,
    ),
}

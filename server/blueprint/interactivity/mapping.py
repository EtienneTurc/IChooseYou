from server.service.command.update.processor import update_command_processor
from server.service.command.create.processor import create_command_processor
from server.blueprint.interactivity.action import BlueprintInteractivityAction
from server.service.formatter.interactivity import (
    format_interactivity_delete_message_payload,
    format_interactivity_edit_workflow_payload,
    format_interactivity_save_workflow_payload,
    format_main_modal_select_command_payload,
    format_main_modal_create_new_command_payload,
    format_main_modal_manage_command_payload,
    format_run_custom_command_payload,
    format_create_command_payload,
    format_update_command_payload,
)
from server.service.slack.interactivity.processor import delete_message_processor
from server.service.slack.modal.enum import SlackModalSubmitAction
from server.service.slack.modal.processor import (
    main_modal_create_command_processor,
    main_modal_update_command_processor,
    main_modal_delete_command_processor,
    main_modal_select_command_processor,
)
from server.service.slack.response.api_response import (
    delete_message_in_channel,
    open_view_modal,
    push_view_modal,
    save_workflow,
    send_message_to_channel,
)
from server.service.slack.workflow.processor import (
    edit_workflow_processor,
    save_workflow_processor,
)
from server.service.command.custom.processor import custom_command_processor

from server.service.tpr.enum import DataFlow
from server.service.error.handler.generic import on_error_handled_send_message


BLUEPRINT_INTERACTIVITY_ACTION_TO_DATA_FLOW = {
    BlueprintInteractivityAction.DELETE_MESSAGE.value: DataFlow(
        formatter=format_interactivity_delete_message_payload,
        processor=delete_message_processor,
        responder=delete_message_in_channel,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.EDIT_WORKFLOW.value: DataFlow(
        formatter=format_interactivity_edit_workflow_payload,
        processor=edit_workflow_processor,
        responder=open_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.VIEW_SUBMISSION.value: DataFlow(  # TODO save workflow with modal action? # noqa E501
        formatter=format_interactivity_save_workflow_payload,
        processor=save_workflow_processor,
        responder=save_workflow,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.MAIN_MODAL_SELECT_COMMAND.value: DataFlow(
        formatter=format_main_modal_select_command_payload,
        processor=main_modal_select_command_processor,
        responder=push_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.MAIN_MODAL_CREATE_NEW_COMMAND.value: DataFlow(
        formatter=format_main_modal_create_new_command_payload,
        processor=main_modal_create_command_processor,
        responder=push_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.MAIN_MODAL_UPDATE_COMMAND.value: DataFlow(
        formatter=format_main_modal_manage_command_payload,
        processor=main_modal_update_command_processor,
        responder=push_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.MAIN_MODAL_DELETE_COMMAND.value: DataFlow(
        formatter=format_main_modal_manage_command_payload,
        processor=main_modal_delete_command_processor,
        responder=send_message_to_channel,
        fast_responder=(lambda **kwargs: {"response_action": "clear"}),  # TODO clean
        error_handler=on_error_handled_send_message,
    ),
    # -------------------------------------------------------------------------
    # ------------------------ SLACK MODAL ACTIONS ----------------------------
    # -------------------------------------------------------------------------
    SlackModalSubmitAction.CREATE_COMMAND.value: DataFlow(
        formatter=format_create_command_payload,
        processor=create_command_processor,
        responder=send_message_to_channel,
        fast_responder=(lambda **kwargs: {"response_action": "clear"}),  # TODO clean
        error_handler=on_error_handled_send_message,
    ),
    SlackModalSubmitAction.UPDATE_COMMAND.value: DataFlow(
        formatter=format_update_command_payload,
        processor=update_command_processor,
        responder=send_message_to_channel,
        fast_responder=(lambda **kwargs: {"response_action": "clear"}),  # TODO clean
        error_handler=on_error_handled_send_message,
    ),
    SlackModalSubmitAction.RUN_CUSTOM_COMMAND.value: DataFlow(
        formatter=format_run_custom_command_payload,
        processor=custom_command_processor,
        responder=send_message_to_channel,
        fast_responder=(lambda **kwargs: {"response_action": "clear"}),  # TODO clean
        error_handler=on_error_handled_send_message,
    ),
}

import functools

from server.blueprint.interactivity.action import (BlueprintInteractivityAction,
                                                   BlueprintInteractivityBlockAction)
from server.service.command.create.processor import create_command_processor
from server.service.command.custom.processor import custom_command_processor
from server.service.command.instant.processor import instant_command_processor
from server.service.command.update.processor import update_command_processor
from server.service.error.handler.generic import on_error_handled_send_message
from server.service.formatter.interactivity import (
    format_create_command_payload, format_interactivity_delete_message_payload,
    format_interactivity_edit_workflow_payload, format_interactivity_resubmit_payload,
    format_interactivity_save_workflow_payload,
    format_main_modal_create_new_command_payload,
    format_main_modal_manage_command_payload,
    format_main_modal_run_instant_command_payload,
    format_main_modal_select_command_payload,
    format_remove_element_from_pick_list_payload, format_run_custom_command_payload,
    format_run_instant_command_modal_block_action, format_run_instant_command_payload,
    format_update_command_payload, format_upsert_modal_block_action)
from server.service.slack.interactivity.processor import (
    delete_message_processor, resubmit_command_and_delete_message_processor)
from server.service.slack.modal.enum import SlackModalSubmitAction
from server.service.slack.modal.processor import (add_element_to_pick_list_processor,
                                                  build_create_command_modal_processor,
                                                  build_custom_command_modal_processor,
                                                  build_delete_command_processor,
                                                  build_instant_command_modal_processor,
                                                  build_update_command_modal_processor,
                                                  open_main_modal_processor,
                                                  remove_element_from_pick_list_processor,
                                                  switch_pick_list_processor)
from server.service.slack.responder.message import (
    send_message_and_gif_to_channel, send_message_and_gif_to_channel_with_resubmit_button)
from server.service.slack.response.api_response import (open_view_modal, push_view_modal,
                                                        save_workflow,
                                                        send_message_to_channel,
                                                        update_view_modal)
from server.service.slack.workflow.processor import (edit_workflow_processor,
                                                     save_workflow_processor)
from server.service.tpr.enum import DataFlow

BLUEPRINT_INTERACTIVITY_ACTION_TO_DATA_FLOW = {
    BlueprintInteractivityAction.DELETE_MESSAGE.value: DataFlow(
        formatter=format_interactivity_delete_message_payload,
        processor=delete_message_processor,
        responder=(lambda **kwargs: None),
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
        processor=build_custom_command_modal_processor,
        responder=push_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.MAIN_MODAL_CREATE_NEW_COMMAND.value: DataFlow(
        formatter=format_main_modal_create_new_command_payload,
        processor=build_create_command_modal_processor,
        responder=push_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.MAIN_MODAL_RUN_INSTANT_COMMAND.value: DataFlow(
        formatter=format_main_modal_run_instant_command_payload,
        processor=build_instant_command_modal_processor,
        responder=push_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.MAIN_MODAL_UPDATE_COMMAND.value: DataFlow(
        formatter=format_main_modal_manage_command_payload,
        processor=build_update_command_modal_processor,
        responder=push_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.MAIN_MODAL_DELETE_COMMAND.value: DataFlow(
        formatter=format_main_modal_manage_command_payload,
        processor=[build_delete_command_processor, open_main_modal_processor],
        responder=[send_message_to_channel, update_view_modal],
        fast_responder=(lambda **kwargs: {"response_action": "clear"}),  # TODO clean
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.RESUBMIT_COMMAND.value: DataFlow(
        formatter=format_interactivity_resubmit_payload,
        processor=functools.partial(
            custom_command_processor, should_update_weight_list=True
        ),
        responder=send_message_and_gif_to_channel_with_resubmit_button,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.RESUBMIT_COMMAND_AND_DELETE_MESSAGE.value: DataFlow(
        formatter=format_interactivity_resubmit_payload,
        processor=resubmit_command_and_delete_message_processor,
        responder=send_message_and_gif_to_channel_with_resubmit_button,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityAction.UPDATE_AND_RESUBMIT_COMMAND.value: DataFlow(
        formatter=format_interactivity_resubmit_payload,
        processor=build_custom_command_modal_processor,
        responder=open_view_modal,
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
        processor=functools.partial(
            custom_command_processor, should_update_weight_list=True
        ),
        responder=send_message_and_gif_to_channel_with_resubmit_button,
        fast_responder=(lambda **kwargs: {"response_action": "clear"}),  # TODO clean
        error_handler=on_error_handled_send_message,
    ),
    SlackModalSubmitAction.RUN_INSTANT_COMMAND.value: DataFlow(
        formatter=format_run_instant_command_payload,
        processor=instant_command_processor,
        responder=send_message_and_gif_to_channel,
        fast_responder=(lambda **kwargs: {"response_action": "clear"}),  # TODO clean
        error_handler=on_error_handled_send_message,
    ),
    # -------------------------------------------------------------------------
    # --------------- BLUEPRINT INTERACTIVITY BLOCK ACTIONS -------------------
    # -------------------------------------------------------------------------
    # Upsert command modal
    BlueprintInteractivityBlockAction.UPSERT_MODAL_SWITCH_PICK_LIST_INPUT.value: DataFlow(
        formatter=format_upsert_modal_block_action,
        processor=lambda **kwargs: switch_pick_list_processor(False, **kwargs),
        responder=update_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityBlockAction.UPSERT_MODAL_ADD_FREE_ELEMENT_TO_PICK_LIST.value: DataFlow(  # noqa E501
        formatter=format_upsert_modal_block_action,
        processor=lambda **kwargs: add_element_to_pick_list_processor(False, **kwargs),
        responder=update_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityBlockAction.UPSERT_MODAL_ADD_USER_TO_PICK_LIST.value: DataFlow(
        formatter=format_upsert_modal_block_action,
        processor=lambda **kwargs: add_element_to_pick_list_processor(False, **kwargs),
        responder=update_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityBlockAction.UPSERT_MODAL_REMOVE_ELEMENT_FROM_PICK_LIST.value: DataFlow(  # noqa E501
        formatter=lambda *args: format_remove_element_from_pick_list_payload(
            False, *args
        ),
        processor=lambda **kwargs: remove_element_from_pick_list_processor(
            False, **kwargs
        ),
        responder=update_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    # Instant command modal
    BlueprintInteractivityBlockAction.INSTANT_COMMAND_MODAL_SWITCH_PICK_LIST_INPUT.value: DataFlow(  # noqa E501
        formatter=format_run_instant_command_modal_block_action,
        processor=lambda **kwargs: switch_pick_list_processor(True, **kwargs),
        responder=update_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityBlockAction.INSTANT_COMMAND_MODAL_ADD_FREE_ELEMENT_TO_PICK_LIST.value: DataFlow(  # noqa E501
        formatter=format_run_instant_command_modal_block_action,
        processor=lambda **kwargs: add_element_to_pick_list_processor(True, **kwargs),
        responder=update_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityBlockAction.INSTANT_COMMAND_MODAL_ADD_USER_TO_PICK_LIST.value: DataFlow(  # noqa E501
        formatter=format_run_instant_command_modal_block_action,
        processor=lambda **kwargs: add_element_to_pick_list_processor(True, **kwargs),
        responder=update_view_modal,
        error_handler=on_error_handled_send_message,
    ),
    BlueprintInteractivityBlockAction.INSTANT_COMMAND_MODAL_REMOVE_ELEMENT_FROM_PICK_LIST.value: DataFlow(  # noqa E501
        formatter=lambda *args: format_remove_element_from_pick_list_payload(
            True, *args
        ),
        processor=lambda **kwargs: remove_element_from_pick_list_processor(
            True, **kwargs
        ),
        responder=update_view_modal,
        error_handler=on_error_handled_send_message,
    ),
}

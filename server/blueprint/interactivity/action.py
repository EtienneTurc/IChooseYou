from enum import Enum

from server.service.slack.modal.main_modal import (SlackMainModalActionId,
                                                   SlackMainModalOverflowActionId)
from server.service.slack.modal.upsert_command_modal import \
    SlackUpsertCommandModalActionId
from server.service.slack.responder.enum import SlackResubmitButtonsActionId


class BlueprintInteractivityAction(Enum):
    RESUBMIT_COMMAND = SlackResubmitButtonsActionId.RESUBMIT_COMMAND.value
    RESUBMIT_COMMAND_AND_DELETE_MESSAGE = (
        SlackResubmitButtonsActionId.RESUBMIT_COMMAND_AND_DELETE_MESSAGE.value
    )
    UPDATE_AND_RESUBMIT_COMMAND = (
        SlackResubmitButtonsActionId.UPDATE_AND_RESUBMIT_COMMAND.value
    )

    DELETE_MESSAGE = "delete_message"  # Defined in slack
    EDIT_WORKFLOW = "workflow_edit"  # Defined in slack TODO change
    VIEW_SUBMISSION = "view_submission"  # Defined by slack

    MAIN_MODAL_SELECT_COMMAND = SlackMainModalActionId.SELECT_COMMAND.value
    MAIN_MODAL_CREATE_NEW_COMMAND = SlackMainModalActionId.CREATE_NEW_COMMAND.value
    MAIN_MODAL_RUN_INSTANT_COMMAND = SlackMainModalActionId.RUN_INSTANT_COMMAND.value
    MAIN_MODAL_UPDATE_COMMAND = SlackMainModalOverflowActionId.UPDATE_COMMAND.value
    MAIN_MODAL_DELETE_COMMAND = SlackMainModalOverflowActionId.DELETE_COMMAND.value


class BlueprintInteractivityBlockAction(Enum):
    UPSERT_MODAL_SWITCH_PICK_LIST_INPUT = (
        SlackUpsertCommandModalActionId.ONLY_USERS_IN_PICK_LIST_CHECKBOX.value
    )
    UPSERT_MODAL_ADD_ELEMENT_TO_PICK_LIST = (
        SlackUpsertCommandModalActionId.FREE_PICK_LIST_INPUT.value
    )
    UPSERT_MODAL_REMOVE_ELEMENT_FROM_PICK_LIST = (
        SlackUpsertCommandModalActionId.REMOVE_FROM_PICK_LIST_BUTTON.value
    )

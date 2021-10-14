from enum import Enum

from server.service.slack.modal.main_modal import (
    SlackMainModalActionId,
    SlackMainModalOverflowActionId,
)


class BlueprintInteractivityAction(Enum):
    RESUBMIT_COMMAND = "resubmit_command"
    DELETE_MESSAGE = "delete_message"  # Defined in slack
    EDIT_WORKFLOW = "workflow_edit"  # Defined in slack TODO change
    VIEW_SUBMISSION = "view_submission"  # Defined by slack

    MAIN_MODAL_SELECT_COMMAND = SlackMainModalActionId.SELECT_COMMAND.value
    MAIN_MODAL_CREATE_NEW_COMMAND = SlackMainModalActionId.CREATE_NEW_COMMAND.value
    MAIN_MODAL_UPDATE_COMMAND = SlackMainModalOverflowActionId.UPDATE_COMMAND.value
    MAIN_MODAL_DELETE_COMMAND = SlackMainModalOverflowActionId.DELETE_COMMAND.value

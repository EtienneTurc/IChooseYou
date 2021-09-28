from enum import Enum

from server.service.slack.modal.main_modal import SlackMainModalActionId


class Action(Enum):
    RESUBMIT_COMMAND = "resubmit_command"
    DELETE_MESSAGE = "delete_message"  # Defined in slack
    WORKFLOW_EDIT = "workflow_edit"  # Defined in slack
    VIEW_SUBMISSION = "view_submission"  # Defined by slack

    MAIN_MODAL_RUN_COMMAND = SlackMainModalActionId.RUN_COMMAND.value
    MAIN_MODAL_CREATE_NEW_COMMAND = SlackMainModalActionId.CREATE_NEW_COMMAND.value

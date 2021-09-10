from enum import Enum


class Action(Enum):
    RESUBMIT_COMMAND = "resubmit_command"
    DELETE_MESSAGE = "delete_message"  # Defined in slack
    WORKFLOW_EDIT = "workflow_edit"  # Defined in slack
    VIEW_SUBMISSION = "view_submission"  # Defined by slack

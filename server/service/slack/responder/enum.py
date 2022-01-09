from enum import Enum


class SlackResubmitButtonsActionId(Enum):
    RESUBMIT_COMMAND = "resubmit_command"
    RESUBMIT_COMMAND_AND_DELETE_MESSAGE = "resubmit_and_delete"
    UPDATE_AND_RESUBMIT_COMMAND = "update_and_resubmit_command"

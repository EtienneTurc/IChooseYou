from enum import Enum


class Action(Enum):
    RESUBMIT_COMMAND = "resubmit_command"
    DELETE_MESSAGE = "delete_message"  # Defined in slack

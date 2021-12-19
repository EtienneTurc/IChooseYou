from enum import Enum


class SlackModalSubmitAction(Enum):
    RUN_CUSTOM_COMMAND = "run_custom_command"
    RUN_INSTANT_COMMAND = "run_instant_command"
    CREATE_COMMAND = "create_command"
    UPDATE_COMMAND = "update_command"


class SlackMainModalActionId(Enum):
    CREATE_NEW_COMMAND = "main_modal_create_new_command"
    RUN_INSTANT_COMMAND = "main_modal_run_instant_command"
    SELECT_COMMAND = "main_modal_select_command"
    MANAGE_COMMAND = "main_modal_manage_command"


class SlackMainModalOverflowActionId(Enum):
    UPDATE_COMMAND = "main_modal_update_command"
    DELETE_COMMAND = "main_modal_delete_command"

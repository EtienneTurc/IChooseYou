from enum import Enum


class WorkflowBlockId(Enum):
    CHANNEL_INPUT = "workflow_block_id_channel"
    COMMAND_INPUT = "workflow_block_id_command"
    SEND_TO_SLACK_CHECKBOX = "workflow_block_id_send_to_slack"


class WorkflowActionId(Enum):
    CHANNEL_INPUT = "workflow_channel_input"
    COMMAND_INPUT = "workflow_command_input"
    SEND_TO_SLACK_CHECKBOX = "workflow_send_to_slack_checkbox"


WORKFLOW_VALUE_PATH = {
    WorkflowActionId.CHANNEL_INPUT.value: f"{WorkflowBlockId.CHANNEL_INPUT.value}.{WorkflowActionId.CHANNEL_INPUT.value}.selected_conversation",  # noqa E501
    WorkflowActionId.COMMAND_INPUT.value: f"{WorkflowBlockId.COMMAND_INPUT.value}.{WorkflowActionId.COMMAND_INPUT.value}.value",  # noqa E501
    WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value: f"{WorkflowBlockId.SEND_TO_SLACK_CHECKBOX.value}.{WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value}.selected_options",  # noqa E501
}

WORKFLOW_ACTION_ID_TO_VARIABLE_NAME = {
    WorkflowActionId.CHANNEL_INPUT.value: "channel_input_value",
    WorkflowActionId.COMMAND_INPUT.value: "command_input_value",
    WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value: "send_to_slack_checkbox_value",
}


class OutputVariable(Enum):
    SELECTED_ITEM = "selected_item"
    SELECTION_MESSAGE = "selection_message"

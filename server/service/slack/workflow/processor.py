from server.service.command.custom.command_line_args import (
    NAMED_ARGS as CUSTOM_NAMED_ARGS,
)
from server.service.command.custom.command_line_args import (
    POSITIONAL_ARG as CUSTOM_POSITIONAL_ARGS,
)
from server.service.command_line.formatter import parse_command_line
from server.service.slack.workflow.edit_modal import build_workflow_edit_modal
from server.service.slack.workflow.enum import OutputVariable, WorkflowActionId
from server.service.slack.workflow.helper import (
    create_select_item_name,
    create_value_dict,
)
from server.service.command.custom.processor import custom_command_processor


def edit_workflow_processor(
    *,
    channel_input_value: str = "",
    command_input_value: str = "",
    send_to_slack_checkbox_value: bool = True,
    **kwargs,
) -> dict[str, any]:
    modal = build_workflow_edit_modal(
        channel_input_value, command_input_value, send_to_slack_checkbox_value
    )
    return {"modal": modal}


def save_workflow_processor(
    *,
    channel_input_value: str = "",
    command_input_value: str = "",
    send_to_slack_checkbox_value: bool = True,
    **kwargs,
) -> dict[str, any]:
    inputs = {
        WorkflowActionId.CHANNEL_INPUT.value: create_value_dict(channel_input_value),
        WorkflowActionId.COMMAND_INPUT.value: create_value_dict(command_input_value),
        WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value: create_value_dict(
            "True" if send_to_slack_checkbox_value else ""
        ),
    }

    command_options = parse_command_line(
        command_input_value, CUSTOM_POSITIONAL_ARGS, CUSTOM_NAMED_ARGS
    )
    number_of_items_to_select = command_options.get("number_of_items_to_select") or 1
    outputs = [
        {
            "name": create_select_item_name(index),
            "type": "text",
            "label": f"Selected item n°{index}",
        }
        for index in range(number_of_items_to_select)
    ]
    outputs.append(
        {
            "name": OutputVariable.SELECTION_MESSAGE.value,
            "type": "text",
            "label": "Selection message",
        }
    )

    return {"inputs": inputs, "outputs": outputs}


def workflow_step_execute_processor(
    *,
    command_name: str,
    team_id: str,
    user_id: str,
    channel_id: str,
    text: str,
    **kwargs,
) -> dict[str, any]:
    custom_command_response = custom_command_processor(
        command_name=command_name,
        channel_id=channel_id,
        team_id=team_id,
        user_id=user_id,
        should_update_weight_list=True,
        **parse_command_line(text, CUSTOM_POSITIONAL_ARGS, CUSTOM_NAMED_ARGS),
    )

    outputs = {}
    for index, selected_item in enumerate(
        custom_command_response.get("selected_items")
    ):
        outputs[create_select_item_name(index)] = selected_item
    outputs[OutputVariable.SELECTION_MESSAGE.value] = (
        custom_command_response.get("message").content
        if custom_command_response.get("message")
        else ""
    )

    return {
        "outputs": outputs,
        "message": custom_command_response.get("message"),
    }

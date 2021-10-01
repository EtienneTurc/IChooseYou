from server.service.tpr.response_format import Response
from server.service.slack.response.response_type import SlackResponseType
from server.service.slack.workflow.edit_modal import build_workflow_edit_modal
from server.service.command_line.formatter import parse_command_line
from server.service.command.custom.command_line_args import (
    POSITIONAL_ARG as CUSTOM_POSITIONAL_ARGS,
    NAMED_ARGS as CUSTOM_NAMED_ARGS,
)
from server.service.slack.workflow.enum import OutputVariable, WorkflowActionId
from server.service.slack.workflow.helper import (
    create_select_item_name,
    create_value_dict,
)


def edit_workflow_processor(
    *,
    channel_input_value: str = "",
    command_input_value: str = "",
    send_to_slack_checkbox_value: bool = True,
    **kwargs,
) -> Response:
    modal = build_workflow_edit_modal(
        channel_input_value, command_input_value, send_to_slack_checkbox_value
    )
    return Response(
        type=SlackResponseType.SLACK_OPEN_VIEW_MODAL.value, data={"modal": modal}
    )


def save_workflow_processor(
    *,
    channel_input_value: str = "",
    command_input_value: str = "",
    send_to_slack_checkbox_value: bool = True,
    **kwargs,
):
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

    return Response(
        type=SlackResponseType.SLACK_SAVE_WORKFLOW,
        data={"inputs": inputs, "outputs": outputs},
    )

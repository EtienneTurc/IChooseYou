from server.service.command.custom.command_line_args import \
    NAMED_ARGS as CUSTOM_NAMED_ARGS
from server.service.command.custom.command_line_args import \
    POSITIONAL_ARG as CUSTOM_POSITIONAL_ARGS
from server.service.command_line.formatter import parse_command_line
from server.service.formatter.interactivity import extract_inputs_from_workflow_payload
from server.service.formatter.slash_command import extract_command_from_text
from server.service.helper.dict_helper import get_by_path
from server.service.slack.workflow.enum import (WORKFLOW_ACTION_ID_TO_VARIABLE_NAME,
                                                WorkflowActionId)


def format_event_basic_payload(payload: dict[str, any]) -> dict[str, any]:
    authorizations = payload.get("authorizations")
    user_id = (
        authorizations[0].get("user_id")
        if authorizations and len(authorizations)
        else None
    )

    return {
        "user_id": user_id,
        "team_id": get_by_path(payload, "team_id"),
        "response_url": "",
    }


def format_event_complete_workflow_payload(payload):
    inputs = extract_inputs_from_workflow_payload(
        get_by_path(payload, "event.workflow_step.inputs")
    )

    command_name, text = extract_command_from_text(
        " ".join(
            inputs.get(
                WORKFLOW_ACTION_ID_TO_VARIABLE_NAME[
                    WorkflowActionId.COMMAND_INPUT.value
                ]
            ).split(" ")[1:]
        )
    )

    workflow_step_execute_id = get_by_path(
        payload, "event.workflow_step.workflow_step_execute_id"
    )

    return {
        "command_name": command_name,
        "workflow_step_execute_id": workflow_step_execute_id,
        "channel_id": inputs.get(
            WORKFLOW_ACTION_ID_TO_VARIABLE_NAME[WorkflowActionId.CHANNEL_INPUT.value]
        ),
        "send_to_slack": inputs.get(
            WORKFLOW_ACTION_ID_TO_VARIABLE_NAME[
                WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value
            ]
        ),
        **parse_command_line(text, CUSTOM_POSITIONAL_ARGS, CUSTOM_NAMED_ARGS),
        **format_event_basic_payload(payload),
    }

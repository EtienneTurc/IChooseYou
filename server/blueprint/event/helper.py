from server.blueprint.slash_command.helper import extract_command_from_text
from server.service.slack.workflow import WorkflowActionId


def format_payload_to_complete_workflow(payload):
    inputs = payload.get("event").get("workflow_step").get("inputs")

    channel_id = inputs[WorkflowActionId.CHANNEL_INPUT.value].get("value")
    send_to_slack = inputs[WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value].get("value")

    input_text = inputs[WorkflowActionId.COMMAND_INPUT.value].get("value")
    command_name, text = extract_command_from_text(" ".join(input_text.split(" ")[1:]))

    authorizations = payload.get("authorizations")
    user_id = (
        authorizations[0].get("user_id")
        if authorizations and len(authorizations)
        else None
    )

    workflow_step_execute_id = (
        payload.get("event").get("workflow_step").get("workflow_step_execute_id")
    )

    return {
        "send_to_slack": send_to_slack,
        "channel": {"id": channel_id, "name": ""},
        "user": {"id": user_id, "name": ""},
        "team_id": payload.get("team_id"),
        "text": text,
        "command_name": command_name,
        "response_url": "",
        "workflow_step_execute_id": workflow_step_execute_id,
    }

from server.blueprint.slash_command.helper import extract_command_from_text
from server.service.error.back_error import BackError
from server.service.helper.dict_helper import get_by_path
from server.service.slack.workflow import WORKFLOW_VALUE_PATH, WorkflowActionId


def format_payload_for_slash_command(payload):
    command_name, text = extract_command_from_text(
        payload.get("actions")[0].get("value")
    )
    return {
        "channel": {
            "id": payload.get("channel").get("id"),
            "name": payload.get("channel").get("name"),
        },
        "user": {
            "id": payload.get("user").get("id"),
            "name": payload.get("user").get("name"),
        },
        "team_id": payload.get("team").get("id"),
        "text": text,
        "command_name": command_name,
        "response_url": payload.get("response_url"),
    }


def format_payload_for_message_delete(payload):
    return {
        "channel_id": payload.get("channel").get("id"),
        "user_id": payload.get("user").get("id"),
        "team_id": payload.get("team").get("id"),
        "text": payload.get("message").get("text"),
        "ts": payload.get("message").get("ts"),
        "response_url": payload.get("response_url"),
    }


def format_payload_for_configuration_modal(payload):
    return {
        "team_id": payload.get("team").get("id"),
        "trigger_id": payload.get("trigger_id"),
        "inputs": payload.get("workflow_step").get("inputs"),
    }


def format_payload_to_save_workflow(payload):
    return {
        "inputs": get_input_from_save_workflow_payload(payload),
        "team_id": payload.get("team").get("id"),
        "workflow_step_edit_id": payload.get("workflow_step").get(
            "workflow_step_edit_id"
        ),
    }


def get_input_from_save_workflow_payload(payload):
    dict = get_by_path(payload, "view.state.values")
    inputs = {}
    for workflow_action in WorkflowActionId:
        value = get_by_path(dict, WORKFLOW_VALUE_PATH[workflow_action.value])

        if workflow_action.value == WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value:
            value = "True" if value and len(value) else ""

        inputs[workflow_action.value] = {
            "value": value,
        }
    return inputs


def assert_message_can_be_delete(text: str, user_id: str) -> bool:
    text_split = text.split("Hey ! <@")
    if len(text_split) <= 1:
        raise BackError("Only pick messages can be deleted.", 400)

    user_id_size = len(user_id)
    expected_user_id = text_split[1][:user_id_size]

    if expected_user_id != user_id:
        message = "Only the user that triggered the slash command can delete"
        message += " the corresponding message."
        raise BackError(message, 400)

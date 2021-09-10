from server.blueprint.slash_command.helper import extract_command_from_text
from server.service.error.back_error import BackError
from server.service.helper.dict_helper import get_by_path
from server.service.slack.workflow import WORKFLOW_VALUE_PATH, WorkflowActionId
from server.service.slack.modal.enum import SlackModalAction
from server.service.slack.modal.custom_command_modal import (
    SlackCustomCommandModalActionId,
    SLACK_CUSTOM_COMMAND_MODAL_VALUE_PATH,
)
from server.orm.command import Command


def format_resubmit_payload_for_slash_command(payload):
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


def format_callback_payload_for_slash_command(
    callback_action: str, id: str, payload: dict[any, any]
):
    callback_action_mapping = {
        SlackModalAction.RUN_CUSTOM_COMMAND.value: format_run_command_payload_for_slash_command  # noqa E501
    }

    return callback_action_mapping[callback_action](id, payload)


def format_run_command_payload_for_slash_command(id: int, payload: dict[any, any]):
    command = Command.find_by_id(id)

    return {
        "user": {
            "id": payload.get("user").get("id"),
            "name": payload.get("user").get("name"),
        },
        "channel_id": command.channel_id,
        "team_id": payload.get("team").get("id"),
        "text": get_text_from_run_command_payload(payload),
        "command_name": command.name,
        "response_url": "",  # TODO
    }


def get_text_from_run_command_payload(payload):
    dict = get_by_path(payload, "view.state.values")
    inputs = {}

    for action in SlackCustomCommandModalActionId:
        value = get_by_path(dict, SLACK_CUSTOM_COMMAND_MODAL_VALUE_PATH[action.value])
        inputs[action.value] = value

    return (
        f"-n {inputs[SlackCustomCommandModalActionId.NUMBER_OF_ITEMS_SELECT.value]}"
        + f" {inputs[SlackCustomCommandModalActionId.ADDITIONAL_TEXT_INPUT.value] or ''}"
    )


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

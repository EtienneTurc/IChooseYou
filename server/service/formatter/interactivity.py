from server.orm.command import Command
from server.blueprint.interactivity.action import BlueprintInteractivityAction
from server.service.helper.dict_helper import get_by_path
from server.service.slack.helper import get_callback_action, get_id_from_callback_id

from server.service.slack.workflow.enum import (
    WORKFLOW_VALUE_PATH,
    WorkflowActionId,
    WORKFLOW_ACTION_ID_TO_VARIABLE_NAME,
)


def extract_interactivity_actions(payload: dict[str, any]) -> tuple[str, str]:
    payload_actions = payload.get("actions")
    actions = [
        payload_actions[0].get("action_id")
        if payload_actions and len(payload_actions)
        else None,
        payload.get("callback_id"),
        payload.get("type"),
    ]

    callback_id = get_by_path(payload, "view.callback_id")
    callback_action = get_callback_action(callback_id)
    return actions, callback_action


def format_interactivity_basic_payload(payload: dict[str, any]) -> dict[str, any]:
    return {
        "channel_id": get_by_path(payload, "channel.id"),
        "user_id": get_by_path(payload, "user.id"),
        "team_id": get_by_path(payload, "team.id"),
        "trigger_id": get_by_path(payload, "trigger_id"),
        "response_url": get_by_path(payload, "response_url"),
    }


def format_interactivity_delete_message_payload(
    payload: dict[str, any]
) -> dict[str, any]:
    return {
        **format_interactivity_basic_payload(payload),
        "message_text": get_by_path(payload, "message.text"),
        "ts": get_by_path(payload, "message.ts"),
    }


def format_interactivity_edit_workflow_payload(
    payload: dict[str, any]
) -> dict[str, any]:
    return {
        **extract_inputs_from_workflow_payload(
            get_by_path(payload, "workflow_step.inputs")
        ),
        **format_interactivity_basic_payload(payload),
    }


def format_interactivity_save_workflow_payload(
    payload: dict[str, any]
) -> dict[str, any]:
    return {
        **extract_inputs_from_workflow_payload(
            get_by_path(payload, "view.state.values")
        ),
        "workflow_step_edit_id": get_by_path(
            payload, "workflow_step.workflow_step_edit_id"
        ),
        **format_interactivity_basic_payload(payload),
    }


def extract_inputs_from_workflow_payload(
    input_payload: dict[str, any]
) -> dict[str, any]:
    inputs = {}
    for workflow_action in WorkflowActionId:
        value = get_by_path(input_payload, WORKFLOW_VALUE_PATH[workflow_action.value])

        if workflow_action.value == WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value:
            value = True if value and len(value) else False

        if value is not None:
            inputs[WORKFLOW_ACTION_ID_TO_VARIABLE_NAME[workflow_action.value]] = value

    return inputs


def format_main_modal_select_command_payload(payload: dict[str, any]) -> dict[str, any]:
    command_id = extract_command_id_from_main_modal_select_command_payload(payload)
    return {
        **get_basic_data_from_command_id(command_id),
        **format_interactivity_basic_payload(payload),
    }


def format_run_custom_command_payload(payload: dict[str, any]) -> dict[str, any]:
    callback_id = get_by_path(payload, "view.callback_id")
    command_id = get_id_from_callback_id(callback_id)
    return {
        **get_basic_data_from_command_id(command_id),
        **format_interactivity_basic_payload(payload),
    }
    # return {"response_action": "clear"}


def extract_command_id_from_main_modal_select_command_payload(
    payload: dict[str, any]
) -> str:
    payload_actions = get_by_path(payload, "actions")

    for action in payload_actions:
        if (
            get_by_path(action, "action_id")
            == BlueprintInteractivityAction.MAIN_MODAL_SELECT_COMMAND.value
        ):
            return get_by_path(action, "value")


def get_basic_data_from_command_id(command_id: str):
    # TODO handle error
    command = Command.find_by_id(command_id)
    return {
        "channel_id": command.channel_id,
        "command_name": command.name,
    }

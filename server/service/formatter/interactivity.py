import json
from enum import Enum

from server.blueprint.interactivity.action import BlueprintInteractivityAction
from server.orm.command import Command
from server.service.helper.dict_helper import clean_none_values, get_by_path
from server.service.slack.helper import get_callback_action, get_id_from_callback_id
from server.service.slack.message_formatting import format_mention_user
from server.service.slack.modal.upsert_command_modal import (
    SLACK_UPSERT_COMMAND_ACTION_ID_TO_VARIABLE_NAME,
    SLACK_UPSERT_COMMAND_MODAL_VALUE_PATH, SlackUpsertCommandModalActionId)
from server.service.slack.workflow.enum import (WORKFLOW_ACTION_ID_TO_VARIABLE_NAME,
                                                WORKFLOW_VALUE_PATH, WorkflowActionId)


def extract_interactivity_actions(payload: dict[str, any]) -> tuple[str, str]:
    payload_actions = payload.get("actions")
    actions = [
        payload_actions[0].get("action_id")
        if payload_actions and len(payload_actions)
        else None,
        get_by_path(payload_actions[0], "selected_option.value").split(".")[0]
        if payload_actions
        and len(payload_actions)
        and get_by_path(payload_actions[0], "selected_option.value")
        else None,
        payload.get("callback_id"),
        payload.get("type"),
    ]

    callback_id = get_by_path(payload, "view.callback_id")
    callback_action = get_callback_action(callback_id) if callback_id else None
    return actions, callback_action


def format_interactivity_basic_payload(payload: dict[str, any]) -> dict[str, any]:
    response_urls = get_by_path(payload, "response_urls")
    data = {
        "channel_id": get_by_path(payload, "channel.id"),
        "user_id": get_by_path(payload, "user.id"),
        "team_id": get_by_path(payload, "team.id"),
        "trigger_id": get_by_path(payload, "trigger_id"),
        "response_url": get_by_path(payload, "response_url")
        or get_by_path(response_urls[0], "response_url")
        if response_urls and len(response_urls)
        else None,
    }
    return clean_none_values(data)


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


def extract_inputs_from_workflow_payload(
    input_payload: dict[str, any]
) -> dict[str, any]:
    inputs = {}
    for workflow_action in WorkflowActionId:
        value = get_by_path(input_payload, f"{workflow_action.value}.value")

        if workflow_action.value == WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value:
            value = True if value and len(value) else False

        if value is not None:
            inputs[WORKFLOW_ACTION_ID_TO_VARIABLE_NAME[workflow_action.value]] = value
    return inputs


def format_interactivity_save_workflow_payload(
    payload: dict[str, any]
) -> dict[str, any]:
    return {
        **extract_inputs_from_view_values_payload(
            get_by_path(payload, "view.state.values"),
            WorkflowActionId,
            WORKFLOW_VALUE_PATH,
            WORKFLOW_ACTION_ID_TO_VARIABLE_NAME,
        ),
        "workflow_step_edit_id": get_by_path(
            payload, "workflow_step.workflow_step_edit_id"
        ),
        **format_interactivity_basic_payload(payload),
    }


def extract_inputs_from_view_values_payload(
    input_payload: dict[str, any],
    actionIdEnum: Enum,
    actionIdToValue: dict[str, any],
    actionIdToVariableName: dict[str, any],
) -> dict[str, any]:
    inputs = {}
    for action in actionIdEnum:
        value = get_by_path(input_payload, actionIdToValue[action.value])

        if action.value.endswith("checkbox"):
            value = True if value and len(value) else False

        if value is not None:
            inputs[actionIdToVariableName[action.value]] = value
    return inputs


def extract_data_from_metadata(private_metadata: str) -> dict[str, any]:
    data = json.loads(private_metadata)
    return clean_none_values(data)


def format_main_modal_select_command_payload(payload: dict[str, any]) -> dict[str, any]:
    command_id = extract_command_id_from_main_modal_select_command_payload(payload)
    return {
        **get_basic_data_from_command_id(command_id),
        **format_interactivity_basic_payload(payload),
    }


def format_main_modal_create_new_command_payload(
    payload: dict[str, any]
) -> dict[str, any]:
    return {
        **extract_data_from_metadata(get_by_path(payload, "view.private_metadata")),
        **format_interactivity_basic_payload(payload),
    }


def format_main_modal_manage_command_payload(payload: dict[str, any]) -> dict[str, any]:
    return {
        "command_id": extract_command_id_from_main_modal_manage_command_payload(
            payload
        ),
        **extract_data_from_metadata(get_by_path(payload, "view.private_metadata")),
        **format_interactivity_basic_payload(payload),
    }


def format_create_command_payload(payload: dict[str, any]) -> dict[str, any]:
    extracted_value = extract_inputs_from_view_values_payload(
        get_by_path(payload, "view.state.values"),
        SlackUpsertCommandModalActionId,
        SLACK_UPSERT_COMMAND_MODAL_VALUE_PATH,
        SLACK_UPSERT_COMMAND_ACTION_ID_TO_VARIABLE_NAME,
    )
    extracted_value["pick_list"] = [
        format_mention_user(user) for user in extracted_value["pick_list"]
    ]

    return {
        **extracted_value,
        **format_interactivity_basic_payload(payload),
    }


def format_update_command_payload(payload: dict[str, any]) -> dict[str, any]:
    extracted_value = extract_inputs_from_view_values_payload(
        get_by_path(payload, "view.state.values"),
        SlackUpsertCommandModalActionId,
        SLACK_UPSERT_COMMAND_MODAL_VALUE_PATH,
        SLACK_UPSERT_COMMAND_ACTION_ID_TO_VARIABLE_NAME,
    )
    extracted_value["pick_list"] = [
        format_mention_user(user) for user in extracted_value["pick_list"]
    ]

    metadata = extract_data_from_metadata(get_by_path(payload, "view.private_metadata"))
    extracted_value["command_to_update"] = metadata["command_name"]
    extracted_value["channel_id"], extracted_value["new_channel_id"] = (
        metadata["channel_id"],
        extracted_value["channel_id"],
    )

    return {
        **extracted_value,
        **format_interactivity_basic_payload(payload),
    }


def format_run_custom_command_payload(payload: dict[str, any]) -> dict[str, any]:
    callback_id = get_by_path(payload, "view.callback_id")
    command_id = get_id_from_callback_id(callback_id)
    return {
        **get_basic_data_from_command_id(command_id),
        **format_interactivity_basic_payload(payload),
    }


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


def extract_command_id_from_main_modal_manage_command_payload(
    payload: dict[str, any]
) -> str:
    payload_actions = get_by_path(payload, "actions")
    action = payload_actions[0]
    value = get_by_path(action, "selected_option.value")
    return value.split(".")[1]


def get_basic_data_from_command_id(command_id: str):
    command = Command.find_by_id(command_id)
    return {
        "channel_id": command.channel_id,
        "command_name": command.name,
    }

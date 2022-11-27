import json
from enum import Enum

from server.blueprint.interactivity.action import BlueprintInteractivityAction
from server.orm.command import Command
from server.service.helper.dict_helper import clean_none_values, get_by_path
from server.service.slack.helper import (get_callback_action, get_id_from_callback_id,
                                         get_index_from_free_pick_list_block_id)
from server.service.slack.modal.custom_command_modal import (
    SLACK_CUSTOM_COMMAND_ACTION_ID_TO_VARIABLE_NAME,
    SLACK_CUSTOM_COMMAND_MODAL_VALUE_PATH, SlackCustomCommandModalActionId)
from server.service.slack.modal.instant_command_modal import (
    SLACK_INSTANT_COMMAND_ACTION_ID_TO_VARIABLE_NAME,
    SLACK_INSTANT_COMMAND_MODAL_VALUE_PATH, SlackInstantCommandModalActionId,
    SlackInstantCommandModalBlockId)
from server.service.slack.modal.upsert_command_modal import (
    SLACK_UPSERT_COMMAND_ACTION_ID_TO_VARIABLE_NAME,
    SLACK_UPSERT_COMMAND_MODAL_VALUE_PATH, SlackUpsertCommandModalActionId,
    SlackUpsertCommandModalBlockId)
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


def format_interactivity_resubmit_payload(payload: dict[str, any]) -> dict[str, any]:
    resubmit_button_value = json.loads(payload.get("actions")[0].get("value"))
    return {**format_interactivity_basic_payload(payload), **resubmit_button_value}


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
    action_id_enum: Enum,
    action_id_to_value: dict[str, any],
    action_id_to_variable_name: dict[str, any],
) -> dict[str, any]:
    inputs = {}
    for action in action_id_enum:
        value = get_by_path(input_payload, action_id_to_value.get(action.value))

        if action.value.endswith("checkbox"):
            value = True if value and len(value) else False

        if value is not None:
            inputs[action_id_to_variable_name[action.value]] = value
        else:
            inputs[action_id_to_variable_name[action.value]] = ""
    return inputs


def extract_pick_list_inputs(
    input_payload: dict[str, any],
    block_id_enum: Enum,
    action_id_enum: Enum,
    action_id_to_value_path: dict[str, any],
):
    return {
        **extract_free_pick_list_input(
            input_payload, block_id_enum, action_id_enum, action_id_to_value_path
        ),
        **extract_user_pick_list_input(
            input_payload, block_id_enum, action_id_enum, action_id_to_value_path
        ),
    }


def extract_free_pick_list_input(
    input_payload: dict[str, any],
    block_id_enum: Enum,
    action_id_enum: Enum,
    action_id_to_value_path: dict[str, any],
) -> dict[str, any]:
    for block_id in input_payload:
        if block_id_enum.FREE_PICK_LIST_BLOCK_ID.value in block_id:
            value = get_by_path(
                input_payload.get(block_id),
                action_id_to_value_path[action_id_enum.FREE_PICK_LIST_INPUT.value],
            )

            return {
                "free_pick_list_item": value,
                "free_pick_list_input_block_id": block_id,
            }
    return {}


def extract_user_pick_list_input(
    input_payload: dict[str, any],
    block_id_enum: Enum,
    action_id_enum: Enum,
    action_id_to_value_path: dict[str, any],
) -> dict[str, any]:
    for block_id in input_payload:
        if block_id_enum.USER_PICK_LIST_BLOCK_ID.value in block_id:
            value = get_by_path(
                input_payload.get(block_id),
                action_id_to_value_path[action_id_enum.USER_PICK_LIST_INPUT.value],
            )

            return {
                "user_pick_list_item": value,
            }
    return {}


def extract_data_from_metadata(private_metadata: str) -> dict[str, any]:
    data = json.loads(private_metadata)
    return clean_none_values(data)


def format_main_modal_select_command_payload(payload: dict[str, any]) -> dict[str, any]:
    command_id = extract_command_id_from_main_modal_select_command_payload(payload)
    return {
        **get_basic_data_from_command_id(command_id),
        **format_interactivity_basic_payload(payload),
    }


def format_main_modal_base_payload(payload: dict[str, any]) -> dict[str, any]:
    return {
        **extract_data_from_metadata(get_by_path(payload, "view.private_metadata")),
        **format_interactivity_basic_payload(payload),
    }


def format_main_modal_clean_deleted_users_payload(
    payload: dict[str, any]
) -> dict[str, any]:
    return {
        "cleaned": True,
        "view_id": get_by_path(payload, "view.id"),
        **format_main_modal_base_payload(payload),
    }


def format_main_modal_manage_command_payload(payload: dict[str, any]) -> dict[str, any]:
    return {
        "command_id": extract_command_id_from_main_modal_manage_command_payload(
            payload
        ),
        "view_id": get_by_path(payload, "view.id"),
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
    metadata = extract_data_from_metadata(get_by_path(payload, "view.private_metadata"))
    extracted_value["pick_list"] = metadata.get("pick_list")

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
    metadata = extract_data_from_metadata(get_by_path(payload, "view.private_metadata"))

    extracted_value["command_to_update"] = metadata.get("command_name")
    extracted_value["channel_id"], extracted_value["new_channel_id"] = (
        metadata.get("channel_id"),
        extracted_value["channel_id"],
    )
    extracted_value["pick_list"] = metadata.get("pick_list")
    extracted_value["user_select_enabled"] = metadata.get("user_select_enabled")

    return {
        **extracted_value,
        **extract_pick_list_inputs(
            get_by_path(payload, "view.state.values"),
            SlackUpsertCommandModalBlockId,
            SlackUpsertCommandModalActionId,
            SLACK_UPSERT_COMMAND_MODAL_VALUE_PATH,
        ),
        **format_interactivity_basic_payload(payload),
    }


def format_run_custom_command_payload(payload: dict[str, any]) -> dict[str, any]:
    extracted_value = extract_inputs_from_view_values_payload(
        get_by_path(payload, "view.state.values"),
        SlackCustomCommandModalActionId,
        SLACK_CUSTOM_COMMAND_MODAL_VALUE_PATH,
        SLACK_CUSTOM_COMMAND_ACTION_ID_TO_VARIABLE_NAME,
    )
    callback_id = get_by_path(payload, "view.callback_id")
    command_id = get_id_from_callback_id(callback_id)
    return {
        **extracted_value,
        **get_basic_data_from_command_id(command_id),
        **format_interactivity_basic_payload(payload),
    }


def format_run_instant_command_payload(payload: dict[str, any]) -> dict[str, any]:
    extracted_value = extract_inputs_from_view_values_payload(
        get_by_path(payload, "view.state.values"),
        SlackInstantCommandModalActionId,
        SLACK_INSTANT_COMMAND_MODAL_VALUE_PATH,
        SLACK_INSTANT_COMMAND_ACTION_ID_TO_VARIABLE_NAME,
    )
    metadata = extract_data_from_metadata(get_by_path(payload, "view.private_metadata"))

    extracted_value["channel_id"] = metadata.get("channel_id")
    extracted_value["pick_list"] = metadata.get("pick_list")
    extracted_value["user_select_enabled"] = metadata.get("user_select_enabled")

    return {
        **extracted_value,
        **extract_pick_list_inputs(
            get_by_path(payload, "view.state.values"),
            SlackInstantCommandModalBlockId,
            SlackInstantCommandModalActionId,
            SLACK_INSTANT_COMMAND_MODAL_VALUE_PATH,
        ),
        **format_interactivity_basic_payload(payload),
    }


def format_run_instant_command_modal_block_action(payload: dict[str, any]):
    return {
        "view_id": get_by_path(payload, "view.id"),
        "callback_id": get_by_path(payload, "view.callback_id"),
        **format_run_instant_command_payload(payload),
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


def format_upsert_modal_block_action(payload: dict[str, any]):
    return {
        "view_id": get_by_path(payload, "view.id"),
        "callback_id": get_by_path(payload, "view.callback_id"),
        **format_update_command_payload(payload),
        **format_interactivity_basic_payload(payload),
    }


def format_remove_element_from_pick_list_payload(
    instant_modal: bool, payload: dict[str, any]
):
    action = payload.get("actions")[0]
    block_id = action.get("block_id")
    index_item_to_remove = get_index_from_free_pick_list_block_id(block_id)
    return {
        "index_item_to_remove": index_item_to_remove,
        **(
            format_run_instant_command_modal_block_action(payload)
            if instant_modal
            else format_upsert_modal_block_action(payload)
        ),
    }

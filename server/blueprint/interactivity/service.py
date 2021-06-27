from server.blueprint.interactivity.action import Action
from server.blueprint.interactivity.helper import (assert_message_can_be_delete,
                                                   format_payload_for_configuration_modal,
                                                   format_payload_for_message_delete,
                                                   format_payload_for_slash_command,
                                                   format_payload_to_save_workflow)
from server.blueprint.slash_command.service import process_slash_command
from server.service.error.decorator import handle_error
from server.service.flask.decorator import make_context
from server.service.helper.thread import launch_function_in_thread
from server.service.slack.sdk_wrapper import (delete_message_in_channel, open_view_modal,
                                              save_workflow_in_slack)
from server.service.slack.workflow import (OutputVariable, WorkflowActionId,
                                           build_workflow_step_edit_modal)


def proccess_interactivity(payload):
    payload_actions = payload.get("actions")
    actions = [
        payload_actions[0].get("action_id")
        if payload_actions and len(payload_actions)
        else None,
        payload.get("callback_id"),
        payload.get("type"),
    ]

    if Action.RESUBMIT_COMMAND.value in actions:
        body = format_payload_for_slash_command(payload)
        return process_slash_command(body)

    elif Action.DELETE_MESSAGE.value in actions:
        body = format_payload_for_message_delete(payload)
        launch_function_in_thread(delete_message, body)
        return ""

    elif Action.WORKFLOW_EDIT.value in actions:
        body = format_payload_for_configuration_modal(payload)
        launch_function_in_thread(open_configuration_modal, body)
        return ""

    elif Action.WORKFLOW_SUBMISSION.value in actions:
        body = format_payload_to_save_workflow(payload)
        launch_function_in_thread(save_workflow, body)
        return ""

    return "Action not handled"


@make_context
@handle_error
def delete_message(
    *, team_id: str, channel_id: str, ts: str, user_id: str, text: str, **kwargs
) -> None:
    assert_message_can_be_delete(text, user_id)
    delete_message_in_channel(team_id, channel_id, ts)


@make_context
@handle_error
def open_configuration_modal(
    *, inputs: dict, team_id: str, trigger_id: str, **kwargs
) -> None:
    initial_channel = inputs.get(WorkflowActionId.CHANNEL_INPUT.value)
    initial_command = inputs.get(WorkflowActionId.COMMAND_INPUT.value)
    send_to_slack_enabled = inputs.get(WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value)
    modal = build_workflow_step_edit_modal(
        initial_channel.get("value") if initial_channel else "",
        initial_command.get("value") if initial_command else "",
        send_to_slack_enabled.get("value") if send_to_slack_enabled else True,
    )
    open_view_modal(modal, trigger_id, team_id)


@make_context
@handle_error
def save_workflow(*, inputs: dict, team_id: str, workflow_step_edit_id: str, **kwargs):
    outputs = [
        {
            "name": OutputVariable.SELECTED_ITEM.value,
            "type": "text",
            "label": "Selected item",
        },
        {
            "name": OutputVariable.SELECTION_MESSAGE.value,
            "type": "text",
            "label": "Selection message",
        },
    ]
    save_workflow_in_slack(inputs, outputs, workflow_step_edit_id, team_id)

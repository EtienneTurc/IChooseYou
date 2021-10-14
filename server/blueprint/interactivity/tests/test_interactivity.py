import io
from contextlib import redirect_stdout

import pytest

import server.service.slack.tests.monkey_patch as monkey_patch  # noqa: F401
from server.blueprint.interactivity.action import BlueprintInteractivityAction
from server.service.slack.workflow.enum import (OutputVariable, WorkflowActionId,
                                                WorkflowBlockId)
from server.service.slack.workflow.helper import create_select_item_name
from server.tests.test_app import *  # noqa: F401, F403

user_id = "4321"


def call_webhook(
    client,
    text="1234",
    callback_id=None,
    action_id=None,
    type=None,
    inputs=None,
    view_state_inputs=None,
):
    f = io.StringIO()
    with redirect_stdout(f):
        response = client.post(
            "/interactivity",
            data=mock_slack_api_data(
                text=text,
                user_id=user_id,
                callback_id=callback_id,
                action_id=action_id,
                type=type,
                inputs=inputs,
                view_state_inputs=view_state_inputs,
            ),
            follow_redirects=True,
        )

    slack_message = f.getvalue()
    return response, slack_message


def mock_slack_api_data(
    team_id="1337",
    channel_id="1234",
    channel_name="youplaboom",
    user_id="4321",
    user_name="patoche",
    text="1234",
    ts="1624201203.000200",
    response_url="https://whatever.com",
    trigger_id="1234",
    workflow_step_edit_id="1234",
    inputs=None,
    callback_id=None,
    action_id=None,
    type=None,
    view_state_inputs=None,
):
    payload = {
        "team": {"id": team_id},
        "user": {"id": user_id, "name": user_name},
        "channel": {"id": channel_id, "name": channel_name},
        "message": {"text": text, "ts": ts},
        "actions": [{"value": text}],
        "response_url": response_url,
        "trigger_id": trigger_id,
        "workflow_step": {"workflow_step_edit_id": workflow_step_edit_id},
    }
    if callback_id:
        payload["callback_id"] = callback_id
    if action_id:
        payload["actions"][0]["action_id"] = action_id
    if type:
        payload["type"] = type
    if inputs:
        payload["workflow_step"]["inputs"] = inputs
    if view_state_inputs:
        payload["view"] = {"state": {"values": view_state_inputs}}

    return {"payload": str(payload).replace("'", '"')}


# @pytest.mark.parametrize(
#     "text, expected",
#     [
#         (
#             "create test_create --pick-list 1 --label test",
#             "Command test_create successfully created.",
#         ),
#         ("help", "Usage"),
#     ],
# )
# def test_interactivity_resubmit_command(text, expected, client):
#     response, slack_message = call_webhook(
#         client, text, action_id=BlueprintInteractivityAction.RESUBMIT_COMMAND.value
#     )
#     assert response.status_code == 200
#     assert expected in slack_message


def test_interactivity_delete_message(client):
    text = f"Hey ! <@{user_id}>"
    response, slack_message = call_webhook(
        client, text, callback_id=BlueprintInteractivityAction.DELETE_MESSAGE.value
    )
    assert response.status_code == 200
    assert "" == slack_message


@pytest.mark.parametrize(
    "text, expected_error_message",
    [
        (
            "blabla bla bla",
            "Only pick messages can be deleted.",
        ),
        (f"<@{user_id}>", "Only pick messages can be deleted."),
        (
            f"Hey ! <@{1 + int(user_id)}>",
            "Only the user that triggered the slash command can delete the corresponding message.",  # noqa E501
        ),
    ],
)
def test_interactivity_delete_message_error(text, expected_error_message, client):
    response, slack_message = call_webhook(
        client, text, callback_id=BlueprintInteractivityAction.DELETE_MESSAGE.value
    )
    assert response.status_code == 200
    assert expected_error_message in slack_message


@pytest.mark.parametrize(
    "inputs, expected_texts",
    [
        (
            {"useless": "useless"},
            [f"'block_id': '{WorkflowBlockId.CHANNEL_INPUT.value}'"],
        ),
        (
            {"useless": "useless"},
            [f"'block_id': '{WorkflowBlockId.COMMAND_INPUT.value}'"],
        ),
        (
            {"useless": "useless"},
            [f"'block_id': '{WorkflowBlockId.SEND_TO_SLACK_CHECKBOX.value}'"],
        ),
        (
            {"useless": "useless"},
            [f"'action_id': '{WorkflowActionId.CHANNEL_INPUT.value}'"],
        ),
        (
            {"useless": "useless"},
            [f"'action_id': '{WorkflowActionId.COMMAND_INPUT.value}'"],
        ),
        (
            {"useless": "useless"},
            [f"'action_id': '{WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value}'"],
        ),
        (
            {f"{WorkflowActionId.CHANNEL_INPUT.value}": {"value": "fake_channel"}},
            ["'initial_conversation': 'fake_channel'"],
        ),
        (
            {f"{WorkflowActionId.COMMAND_INPUT.value}": {"value": "fake_command"}},
            ["'initial_value': 'fake_command'"],
        ),
        (
            {f"{WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value}": {"value": "True"}},
            ["'initial_options': [{'text':"],
        ),
        (
            {
                f"{WorkflowActionId.CHANNEL_INPUT.value}": {"value": "fake_channel"},
                f"{WorkflowActionId.COMMAND_INPUT.value}": {"value": "fake_command"},
                f"{WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value}": {"value": "True"},
            },
            ["fake_channel", "fake_command"],
        ),
    ],
)
def test_interactivity_open_conversation_modal(
    inputs: dict, expected_texts: list[str], client
):
    response, slack_message = call_webhook(
        client, type=BlueprintInteractivityAction.EDIT_WORKFLOW.value, inputs=inputs
    )
    assert response.status_code == 200
    for text in expected_texts:
        assert text in slack_message


@pytest.mark.parametrize(
    "view_state_inputs, expected_texts",
    [
        (
            {
                WorkflowBlockId.CHANNEL_INPUT.value: {
                    WorkflowActionId.CHANNEL_INPUT.value: {
                        "selected_conversation": "fake_conversation_selected"
                    }
                }
            },
            ["fake_conversation_selected"],
        ),
        (
            {
                WorkflowBlockId.COMMAND_INPUT.value: {
                    WorkflowActionId.COMMAND_INPUT.value: {
                        "value": "fake_command_given"
                    }
                }
            },
            ["fake_command_given"],
        ),
        (
            {
                WorkflowBlockId.COMMAND_INPUT.value: {
                    WorkflowActionId.COMMAND_INPUT.value: {
                        "value": "fake_command_given -n 2"
                    }
                }
            },
            [create_select_item_name(0), create_select_item_name(1)],
        ),
        (
            {
                WorkflowBlockId.SEND_TO_SLACK_CHECKBOX.value: {
                    WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value: {
                        "selected_options": [{"text": "whatever"}]
                    }
                }
            },
            ["True"],
        ),
        (
            {
                WorkflowBlockId.SEND_TO_SLACK_CHECKBOX.value: {
                    WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value: {
                        "selected_options": [{"text": "whatever"}]
                    }
                }
            },
            [OutputVariable.SELECTED_ITEM.value],
        ),
        (
            {
                WorkflowBlockId.SEND_TO_SLACK_CHECKBOX.value: {
                    WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value: {
                        "selected_options": [{"text": "whatever"}]
                    }
                }
            },
            [OutputVariable.SELECTION_MESSAGE.value],
        ),
    ],
)
def test_interactivity_save_workflow(view_state_inputs, expected_texts, client):
    response, slack_message = call_webhook(
        client,
        type=BlueprintInteractivityAction.VIEW_SUBMISSION.value,
        view_state_inputs=view_state_inputs,
    )
    assert response.status_code == 200
    for text in expected_texts:
        assert text in slack_message

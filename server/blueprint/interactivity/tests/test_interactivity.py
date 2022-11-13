import pytest

from server.blueprint.interactivity.action import BlueprintInteractivityAction
from server.blueprint.interactivity.tests.helper import call_webhook
from server.service.slack.tests.monkey_patch import *  # noqa: F401, F403
from server.service.slack.workflow.enum import (OutputVariable, WorkflowActionId,
                                                WorkflowBlockId)
from server.service.slack.workflow.helper import create_select_item_name
from server.tests.test_app import *  # noqa: F401, F403

user_id = "4321"


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
        client,
        text=text,
        user_id=user_id,
        callback_id=BlueprintInteractivityAction.DELETE_MESSAGE.value,
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
        client,
        text=text,
        user_id=user_id,
        callback_id=BlueprintInteractivityAction.DELETE_MESSAGE.value,
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

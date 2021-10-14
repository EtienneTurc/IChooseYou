import io
from contextlib import redirect_stdout

import pytest

import server.service.slack.tests.monkey_patch as monkey_patch  # noqa: F401
from server.blueprint.event.tests.conftest import (
    TEST_COMMAND_CHANNEL_ID,
    TEST_COMMAND_LABEL,
    TEST_COMMAND_NAME,
    TEST_COMMAND_PICK_LIST,
)
from server.blueprint.event.action import BlueprintEventAction
from server.service.slack.workflow.enum import (
    OutputVariable,
    WorkflowActionId,
)
from server.service.slack.workflow.helper import create_select_item_name
from server.tests.test_app import *  # noqa: F401, F403
from server.tests.test_fixture import *  # noqa: F401, F403

extra_text = "here is some extra text"


def call_webhook(
    client,
    event_type=None,
    inputs=None,
):
    f = io.StringIO()
    with redirect_stdout(f):
        response = client.post(
            "/event",
            data=mock_slack_api_data(
                event_type=event_type,
                inputs=inputs,
            ),
            follow_redirects=True,
        )

    slack_message = f.getvalue()
    return response, slack_message


def mock_slack_api_data(
    team_id="1337",
    user_id="4321",
    workflow_step_execute_id="1234",
    event_type=None,
    inputs=None,
):
    payload = {
        "team_id": team_id,
        "event": {
            "type": event_type,
            "workflow_step": {
                "inputs": inputs,
                "workflow_step_execute_id": workflow_step_execute_id,
            },
        },
        "authorizations": [{"user_id": user_id}],
    }

    return str(payload).replace("'", '"')


@pytest.mark.parametrize(
    "expected_text",
    [
        "Hey !",
        TEST_COMMAND_LABEL,
        extra_text,
    ],
)
def test_event_workflow_complete(expected_text, client, test_command):
    inputs = {
        WorkflowActionId.CHANNEL_INPUT.value: {"value": TEST_COMMAND_CHANNEL_ID},
        WorkflowActionId.COMMAND_INPUT.value: {
            "value": f"/ichu {TEST_COMMAND_NAME} {extra_text}"
        },
        WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value: {"value": "true"},
    }
    response, slack_message = call_webhook(
        client,
        event_type=BlueprintEventAction.WORKFLOW_STEP_EXECUTE.value,
        inputs=inputs,
    )
    assert response.status_code == 200
    assert expected_text in slack_message


@pytest.mark.parametrize(
    "command, expected_text",
    [
        (f"/ichu {TEST_COMMAND_NAME}", "Hey !"),
        (f"/ichu {TEST_COMMAND_NAME}", TEST_COMMAND_LABEL),
        (f"/ichu {TEST_COMMAND_NAME} {extra_text}", extra_text),
        (f"/ichu {TEST_COMMAND_NAME}", OutputVariable.SELECTED_ITEM.value),
        (f"/ichu {TEST_COMMAND_NAME}", OutputVariable.SELECTION_MESSAGE.value),
        (f"/ichu {TEST_COMMAND_NAME} -n 2", create_select_item_name(0)),
        (f"/ichu {TEST_COMMAND_NAME} -n 2", create_select_item_name(1)),
        (
            f"/ichu {TEST_COMMAND_NAME} -n 2",
            f"'{create_select_item_name(0)}': '{TEST_COMMAND_PICK_LIST[1]}'",
        ),
        (
            f"/ichu {TEST_COMMAND_NAME} -n 2",
            f"'{create_select_item_name(1)}': '{TEST_COMMAND_PICK_LIST[2]}'",
        ),
    ],
)
def test_event_workflow_complete_output(
    command, expected_text, client, test_command, set_seed
):
    inputs = {
        WorkflowActionId.CHANNEL_INPUT.value: {"value": TEST_COMMAND_CHANNEL_ID},
        WorkflowActionId.COMMAND_INPUT.value: {"value": command},
        WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value: {"value": ""},
    }
    response, slack_message = call_webhook(
        client,
        event_type=BlueprintEventAction.WORKFLOW_STEP_EXECUTE.value,
        inputs=inputs,
    )
    assert response.status_code == 200
    assert expected_text in slack_message


@pytest.mark.parametrize(
    "inputs, expected_texts",
    [
        (
            {
                WorkflowActionId.CHANNEL_INPUT.value: {
                    "value": TEST_COMMAND_CHANNEL_ID
                },
                WorkflowActionId.COMMAND_INPUT.value: {
                    "value": f"/ichu fake_{TEST_COMMAND_NAME} {extra_text}"
                },
                WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value: {"value": ""},
            },
            [f"Command fake_{TEST_COMMAND_NAME} does not exist"],
        ),
        (
            {
                WorkflowActionId.CHANNEL_INPUT.value: {
                    "value": f"fake_{TEST_COMMAND_CHANNEL_ID}"
                },
                WorkflowActionId.COMMAND_INPUT.value: {
                    "value": f"/ichu {TEST_COMMAND_NAME} {extra_text}"
                },
                WorkflowActionId.SEND_TO_SLACK_CHECKBOX.value: {"value": ""},
            },
            [f"Command {TEST_COMMAND_NAME} does not exist"],
        ),
    ],
)
def test_event_workflow_fail(inputs, expected_texts, client, test_command):
    response, slack_message = call_webhook(
        client,
        event_type=BlueprintEventAction.WORKFLOW_STEP_EXECUTE.value,
        inputs=inputs,
    )
    assert response.status_code == 200
    for expected_text in expected_texts:
        assert expected_text in slack_message

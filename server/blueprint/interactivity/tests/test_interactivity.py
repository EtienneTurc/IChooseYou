import io
from contextlib import redirect_stdout

import pytest

import server.service.slack.tests.monkey_patch as monkey_patch  # noqa: F401
from server.blueprint.interactivity.action import Action
from server.tests.test_app import *  # noqa: F401, F403

user_id = "4321"


def call_webhook(client, text, callback_id=None, action_id=None):
    f = io.StringIO()
    with redirect_stdout(f):
        response = client.post(
            "/interactivity",
            data=mock_slack_api_data(
                text=text, user_id=user_id, callback_id=callback_id, action_id=action_id
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
    callback_id=None,
    action_id=None,
):
    payload = {
        "team": {"id": team_id},
        "user": {"id": user_id, "name": user_name},
        "channel": {"id": channel_id, "name": channel_name},
        "message": {"text": text, "ts": ts},
        "actions": [{"value": text}],
        "response_url": response_url,
    }
    if callback_id:
        payload["callback_id"] = callback_id
    if action_id:
        payload["actions"][0]["action_id"] = action_id

    return {"payload": str(payload).replace("'", '"')}


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "create test_create --pick-list 1 --label test",
            "Command test_create successfully created.",
        ),
        ("help", "Usage"),
    ],
)
def test_interactivity_resubmit_command(text, expected, client):
    response, slack_message = call_webhook(
        client, text, action_id=Action.RESUBMIT_COMMAND.value
    )
    assert response.status_code == 200
    assert expected in slack_message


def test_interactivity_delete_message(client):
    text = f"Hey ! <@{user_id}>"
    response, slack_message = call_webhook(
        client, text, callback_id=Action.DELETE_MESSAGE.value
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
        client, text, callback_id=Action.DELETE_MESSAGE.value
    )
    assert response.status_code == 200
    assert expected_error_message in slack_message

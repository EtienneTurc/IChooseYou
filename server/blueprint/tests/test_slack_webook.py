import io
from contextlib import redirect_stdout

import pytest

import server.blueprint.tests.monkey_patch as monkey_patch  # noqa: F401
import server.slack.tests.monkey_patch_request as monkey_patch_request  # noqa: F401
from server.orm.command import Command
from server.tests.test_app import *  # noqa: F401, F403


def call_webhook(client, text):
    f = io.StringIO()
    with redirect_stdout(f):
        response = client.post(
            "/slack_webhook",
            data=mock_slack_webhook_data(text=text),
            follow_redirects=True,
        )

    slack_message = f.getvalue()
    return response, slack_message


def mock_slack_webhook_data(
    channel_id="1234",
    channel_name="1234",
    user_id="4321",
    user_name="1234",
    text="1234",
    response_url="1234",
):
    return {
        "channel_id": channel_id,
        "channel_name": channel_name,
        "user_id": user_id,
        "user_name": user_name,
        "text": text,
        "response_url": response_url,
    }


def test_slack_webhook_no_command(client):
    text = ""
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert "No command found." in slack_message


@pytest.mark.parametrize(
    "text",
    [
        "create test_create --pickList 1 --label test",
        "create test_create --pickList 1 2 3 --label test create",
        "create test_create --pickList 1 2 3 --label test create --selfExclude",  # noqa: E501
        "create test_create --pickList 1 2 3 --label test create --selfExclude True",  # noqa: E501
    ],
)
def test_slack_webhook_create(text, client):
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert "Command test_create successfully created." in slack_message


@pytest.mark.parametrize(
    "text",
    [
        "create test_create",
        "create test_create --pickList 1 2 3",
        "create test_create --label 1 2 3",
        "create --pickList 1 2 3 --label 1 2 3",
    ],
)
def test_slack_webhook_create_fail(text, client):
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert "create: error: the following arguments are required:" in slack_message


@pytest.mark.parametrize(
    "text",
    [
        "create --commandName test_create --pickList 1 2 3 --label 1 2 3",
    ],
)
def test_slack_webhook_create_fail_unrecognized_element(text, client):
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert "create: error: unrecognized arguments:" in slack_message


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "update test_update --pickList 1 2 3",
            {"pick_list": ["1", "2", "3"]},
        ),
        (
            "update test_update --addToPickList 1 2 3 4",
            {"pick_list": ["1", "2", "3", "4"]},
        ),
        (
            "update test_update --removeFromPickList 1 2 3 4",
            {"pick_list": []},
        ),
        ("update test_update --label My label", {"label": "My label"}),
        ("update test_update --label My label", {"self_exclude": True}),
        ("update test_update --selfExclude", {"self_exclude": True}),
        (
            "update test_update --selfExclude True",
            {"self_exclude": True},
        ),
        (
            "update test_update --selfExclude False",
            {"self_exclude": False},
        ),
    ],
)
def test_slack_webhook_update(text, expected, client):
    Command.create("test_update", "1234", "label", ["1", "2"], True, "4321")
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "Command test_update successfully updated." in slack_message

    updated_command = (
        Command.find_one_by_name_and_chanel("test_update", "1234").to_son().to_dict()
    )

    for key in expected:
        func_to_apply = lambda x: x  # noqa: E731
        if type(expected[key]) == list:
            func_to_apply = sorted
        assert func_to_apply(updated_command[key]) == func_to_apply(expected[key])


def test_slack_webhook_delete(client):
    Command.create("test_delete", "1234", "label", ["1", "2"], False, "4321")
    text = "delete test_delete"
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "Command test_delete successfully deleted." in slack_message

    with pytest.raises(Command.DoesNotExist):
        Command.find_one_by_name_and_chanel("test_delete", "1234", catch=False)


def test_slack_webhook_delete_fail(client):
    Command.create("test_delete", "1234", "label", ["1", "2"], False, "4321")
    text = "delete test_delete_unknown_command"
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "Command test_delete_unknown_command does not exist" in slack_message

    command = Command.find_one_by_name_and_chanel("test_delete", "1234")
    assert command is not None


def test_slack_webhook_custom(client):
    Command.create("test_custom", "1234", "label", ["pick_1", "pick_2"], False, "4321")
    text = "test_custom"
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "Hey !" in slack_message


def test_slack_webhook_no_custom_command(client):
    text = "test_custom"
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert "Command test_custom does not exist." in slack_message

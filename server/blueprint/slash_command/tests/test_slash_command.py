import io
from contextlib import redirect_stdout

import pytest

import server.service.slack.tests.monkey_patch as monkey_patch  # noqa: F401
from server.orm.command import Command
from server.tests.test_app import *  # noqa: F401, F403


def call_webhook(client, text):
    f = io.StringIO()
    with redirect_stdout(f):
        response = client.post(
            "/slash_command",
            data=mock_slack_api_data(text=text),
            follow_redirects=True,
        )

    slack_message = f.getvalue()
    return response, slack_message


def mock_slack_api_data(
    team_id="1337",
    channel_id="1234",
    channel_name="1234",
    user_id="4321",
    user_name="1234",
    text="1234",
    response_url="https://whatever.com",
):
    return {
        "team_id": team_id,
        "channel_id": channel_id,
        "channel_name": channel_name,
        "user_id": user_id,
        "user_name": user_name,
        "text": text,
        "response_url": response_url,
    }


def test_slash_command_no_command(client):
    text = ""
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert "No command found." in slack_message


@pytest.mark.parametrize(
    "text",
    [
        "create test_create --pick-list 1 --label test",
        "create test_create --pick-list 1 2 3 --label test create",
        "create test_create --pick-list 1 2 3 --label test create --self-exclude",  # noqa: E501
        "create test_create --pick-list 1 2 3 --label test create --self-exclude True",  # noqa: E501
        "create test_create --pick-list 1 2 3 --label test create -o",  # noqa: E501
    ],
)
def test_slash_command_create(text, client):
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert "Command test_create successfully created." in slack_message


@pytest.mark.parametrize(
    "text",
    [
        "create test_create",
        "create test_create --pick-list 1 2 3",
        "create test_create --label 1 2 3",
        "create --pick-list 1 2 3 --label 1 2 3",
    ],
)
def test_slash_command_create_fail(text, client):
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert "create: error: the following arguments are required:" in slack_message


@pytest.mark.parametrize(
    "text",
    [
        "create --commandName test_create --pick-list 1 2 3 --label 1 2 3",
    ],
)
def test_slash_command_create_fail_unrecognized_element(text, client):
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert "create: error: unrecognized arguments:" in slack_message


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "update test_update --pick-list 1 2 3",
            {"pick_list": ["1", "2", "3"]},
        ),
        (
            "update test_update --add-to-pick-list 1 2 3 4",
            {"pick_list": ["1", "2", "3", "4"]},
        ),
        (
            "update test_update --remove-from-pick-list 1 2 3 4",
            {"pick_list": []},
        ),
        ("update test_update --label My label", {"label": "My label"}),
        ("update test_update --label My label", {"self_exclude": True}),
        ("update test_update --self-exclude", {"self_exclude": True}),
        (
            "update test_update --self-exclude True",
            {"self_exclude": True},
        ),
        (
            "update test_update --self-exclude False",
            {"self_exclude": False},
        ),
        (
            "update test_update -o",
            {"only_active_users": True},
        ),
    ],
)
def test_slash_command_update(text, expected, client):
    Command.create(
        name="test_update",
        channel_id="1234",
        label="label",
        pick_list=["1", "2"],
        self_exclude=True,
        only_active_users=False,
        created_by_user_id="4321",
    )
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


def test_slash_command_delete(client):
    Command.create(
        name="test_delete",
        channel_id="1234",
        label="label",
        pick_list=["1", "2"],
        self_exclude=True,
        only_active_users=False,
        created_by_user_id="4321",
    )
    text = "delete test_delete"
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "Command test_delete successfully deleted." in slack_message

    with pytest.raises(Command.DoesNotExist):
        Command.find_one_by_name_and_chanel("test_delete", "1234", catch=False)


def test_slash_command_delete_fail(client):
    Command.create(
        name="test_delete",
        channel_id="1234",
        label="label",
        pick_list=["1", "2"],
        self_exclude=True,
        only_active_users=False,
        created_by_user_id="4321",
    )
    text = "delete test_delete_unknown_command"
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "Command test_delete_unknown_command does not exist" in slack_message

    command = Command.find_one_by_name_and_chanel("test_delete", "1234")
    assert command is not None


def test_slash_command_custom(client):
    Command.create(
        name="test_custom",
        channel_id="1234",
        label="label",
        pick_list=["pick_1", "pick_2"],
        self_exclude=False,
        only_active_users=False,
        created_by_user_id="4321",
    )
    text = "test_custom"
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "Hey !" in slack_message


def test_slash_command_no_custom_command(client):
    text = "test_custom"
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert "Command test_custom does not exist." in slack_message

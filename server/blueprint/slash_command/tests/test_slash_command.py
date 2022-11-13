import io
from contextlib import redirect_stdout

import pytest

import server.service.slack.tests.monkey_patch as monkey_patch  # noqa: F401
from server.orm.command import Command
from server.service.strategy.enum import Strategy
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
    assert "4321 created *test_create*." in slack_message


@pytest.mark.parametrize(
    "text, expected_message",
    [
        (
            "create test_create",
            "Field 'pick_list' is not valid. Failed with error: ['Missing data for required field.']",  # noqa E501
        ),
        (
            "create test_create --label 1 2 3",
            "Field 'pick_list' is not valid. Failed with error: ['Missing data for required field.']",  # noqa E501
        ),
        (
            "create --pick-list 1 2 3 --label 1 2 3",
            "Field 'new_command_name' is not valid. Failed with error: ['Missing data for required field.']",  # noqa E501
        ),
    ],
)
def test_slash_command_create_fail(text, expected_message, client):
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert expected_message in slack_message


@pytest.mark.parametrize(
    "text",
    [
        "create --commandName test_create --pick-list 1 2 3 --label 1 2 3",
    ],
)
def test_slash_command_create_fail_unrecognized_element(text, client):
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert (
        "Field 'new_command_name' is not valid. Failed with error: ['Missing data for required field.']"  # noqa E501
        in slack_message
    )


@pytest.mark.parametrize(
    "text, expected",
    [
        ("update test_update --label My label", {"label": "My label"}),
        (
            "update test_update --description new description",
            {"label": "label", "description": "new description"},
        ),
        (
            "update test_update --pick-list 1 2 3",
            {"pick_list": ["1", "2", "3"]},
        ),
        (
            "update test_update --add-to-pick-list 1 2 3 4",
            {"pick_list": ["1", "2", "3", "4"]},
        ),
        (
            "update test_update --remove-from-pick-list 2 3 4",
            {"pick_list": ["1"]},
        ),
        ("update test_update --label My label", {"self_exclude": True}),
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
        description="description",
        pick_list=["1", "2"],
        weight_list=[1 / 2, 1 / 2],
        strategy=Strategy.uniform.name,
        self_exclude=True,
        only_active_users=False,
        created_by_user_id="4321",
    )
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "4321 updated *test_update*." in slack_message

    updated_command = (
        Command.find_one_by_name_and_chanel("test_update", "1234").to_son().to_dict()
    )

    for key in expected:
        func_to_apply = lambda x: x  # noqa: E731
        if type(expected[key]) == list:
            func_to_apply = sorted
        assert func_to_apply(updated_command[key]) == func_to_apply(expected[key])


@pytest.mark.parametrize(
    "text",
    [
        "update test_update",
        "update test_update --pick-list 1 2",
        "update test_update --label label",
        "update test_update --description description",
        "update test_update --strategy uniform",
        "update test_update --self-exclude",
        "update test_update --only-active-users False",
    ],
)
def test_slash_command_no_changes(text, client):
    Command.create(
        name="test_update",
        channel_id="1234",
        label="label",
        description="description",
        pick_list=["1", "2"],
        weight_list=[1 / 2, 1 / 2],
        strategy=Strategy.uniform.name,
        self_exclude=True,
        only_active_users=False,
        created_by_user_id="4321",
    )
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "Nothing to update for command *test_update*." in slack_message


def test_slash_command_delete(client):
    Command.create(
        name="test_delete",
        channel_id="1234",
        label="label",
        description="description",
        pick_list=["1", "2"],
        weight_list=[1 / 2, 1 / 2],
        strategy=Strategy.uniform.name,
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
        description="description",
        pick_list=["1", "2"],
        weight_list=[1 / 2, 1 / 2],
        strategy=Strategy.uniform.name,
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
        description="description",
        pick_list=["pick_1", "pick_2"],
        weight_list=[1 / 2, 1 / 2],
        strategy=Strategy.uniform.name,
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


def test_slash_command_custom_update_weight_list(client):
    name = "test_custom"
    channel_id = "1234"
    Command.create(
        name="test_custom",
        channel_id="1234",
        label="label",
        description="description",
        pick_list=["pick_1", "pick_2"],
        weight_list=[1, 0],
        strategy=Strategy.round_robin.name,
        self_exclude=False,
        only_active_users=False,
        created_by_user_id="4321",
    )
    response, slack_message = call_webhook(client, name)

    assert response.status_code == 200
    assert "Hey !" in slack_message

    command = Command.find_one_by_name_and_chanel(name=name, channel_id=channel_id)
    assert command.weight_list == [0, 1]


def test_slash_command_custom_multi_select(client):
    command_name = "test_custom"
    text = f"{command_name} -n 2"
    channel_id = "1234"
    Command.create(
        name=command_name,
        channel_id="1234",
        label="label",
        description="description",
        pick_list=["pick_1", "pick_2"],
        weight_list=[1, 0],
        strategy=Strategy.round_robin.name,
        self_exclude=False,
        only_active_users=False,
        created_by_user_id="4321",
    )
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "pick_1 and pick_2" in slack_message

    command = Command.find_one_by_name_and_chanel(
        name=command_name, channel_id=channel_id
    )
    assert command.weight_list == [1, 0]


def test_slash_command_custom_with_wheel(client):
    Command.create(
        name="test_custom",
        channel_id="1234",
        label="label",
        description="description",
        pick_list=["pick_1", "pick_2"],
        weight_list=[1 / 2, 1 / 2],
        strategy=Strategy.uniform.name,
        self_exclude=False,
        only_active_users=False,
        created_by_user_id="4321",
    )
    text = "test_custom -w"
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "Spin that wheel :ferris_wheel:" in slack_message
    assert "File wheel.gif uploaded" in slack_message
    assert "Hey !" in slack_message


@pytest.mark.parametrize(
    "text, expected",
    [
        ("instant --pick-list 1", "Hey ! "),
        ("instant --pick-list 1", "choose 1"),
        ("instant --pick-list 1 -n 2", "choose 1 and 1"),
        ("instant --pick-list 1 -w", "Spin that wheel :ferris_wheel:"),
        ("instant --pick-list 1 -w", "File wheel.gif uploaded"),
    ],
)
def test_slash_command_instant(text, expected, client):
    response, slack_message = call_webhook(client, text)
    assert response.status_code == 200
    assert expected in slack_message


def test_slash_command_clean_deleted_users(client):
    Command.create(
        name="test_delete",
        channel_id="1234",
        label="label",
        description="description",
        pick_list=["<@1234>", "<@deleted>"],
        weight_list=[1 / 2, 1 / 2],
        strategy=Strategy.uniform.name,
        self_exclude=True,
        only_active_users=False,
        created_by_user_id="4321",
    )

    text = "clean_deleted_users"
    response, slack_message = call_webhook(client, text)

    assert response.status_code == 200
    assert "cleaned up the deleted users from the pick lists :broom:" in slack_message

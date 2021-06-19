import pytest

import server.service.slack.tests.monkey_patch_request as monkey_patch_request  # noqa: F401, E501
from server.orm.command import Command
from server.service.command.args import ArgError
from server.service.command.update import UpdateCommand
from server.service.slack.message import MessageStatus, MessageVisibility
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "1234"
user_id = "4321"
team_id = "1337"


@pytest.mark.parametrize(
    "text, expected_message",
    [
        (
            "test_update --label my new label",
            "Command test_update successfully updated.",
        ),
        (
            "test_update -l my new label",
            "Command test_update successfully updated.",
        ),
        (
            "test_update --label my new label",
            "my new label",
        ),
        (
            "test_update -l my new label",
            "my new label",
        ),
        (
            "test_update --pick-list 1 2 3",
            "['1', '2', '3']",
        ),
        (
            "test_update -p 1 2 3",
            "['1', '2', '3']",
        ),
        (
            "test_update --pick-list all_members",
            "['<@1234>', '<@2345>', '<@3456>']",
        ),
        (
            "test_update --add-to-pick-list 3",
            "'3'",
        ),
        (
            "test_update -a 3",
            "'3'",
        ),
        (
            "test_update --remove-from-pick-list 1",
            "['2']",
        ),
        (
            "test_update -r 1",
            "['2']",
        ),
        (
            "test_update --label my new label",
            "User using the slash command excluded.",
        ),
        (
            "test_update --label my new label --self-exclude",
            "User using the slash command excluded.",
        ),
        (
            "test_update --label my new label --self-exclude True",
            "User using the slash command excluded.",
        ),
        (
            "test_update --label my new label --self-exclude False",
            "User using the slash command not excluded.",
        ),
    ],
)
def test_update(text, expected_message, client):
    Command.create(
        name="test_update",
        channel_id=channel_id,
        label="label",
        pick_list=["1", "2"],
        self_exclude=True,
        only_active_users=False,
        created_by_user_id=user_id,
    )
    message = UpdateCommand(text=text, team_id=team_id, channel_id=channel_id).exec(
        user_id
    )
    assert expected_message in message.content
    assert message.status == MessageStatus.SUCCESS
    assert message.visibility == MessageVisibility.NORMAL


@pytest.mark.parametrize("text", ["-h", "--help", "whatever -h"])
def test_create_help(text, client):
    message = UpdateCommand(text=text, team_id=team_id, channel_id=channel_id).exec(
        user_id
    )
    assert "Update a given command." in message.content
    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.HIDDEN


def test_update_fail_if_command_does_not_exist(client):
    text = "test_update --label my label --pick-list 1 2 3 --self-exclude"

    with pytest.raises(ArgError, match="Command test_update does not exist."):
        UpdateCommand(text=text, team_id=team_id, channel_id=channel_id).exec(user_id)

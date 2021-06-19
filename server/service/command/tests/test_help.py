from server.orm.command import Command
from server.service.command.help import HelpCommand
from server.service.slack.message import MessageStatus, MessageVisibility
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "1234"
team_id = "1337"


def test_help_with_no_commands(client):
    text = ""
    Command.create(
        name="test_help",
        channel_id=channel_id,
        label="my fancy label",
        pick_list=["1", "2"],
        self_exclude=True,
        only_active_users=False,
        created_by_user_id="4321",
    )
    message = HelpCommand(text=text, team_id=team_id, channel_id=channel_id).exec()

    expected_texts = [
        "create",
        "update",
        "delete",
        "help",
        "_*Fixed commands:*_\n",
        "\n _*Created commands:*_\n",
        "Usage",
        "test_help",
        "my fancy label",
    ]
    for expected_text in expected_texts:
        assert expected_text in message.content
    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.HIDDEN


def test_help_with_given_known_command(client):
    text = "create"
    message = HelpCommand(text=text, team_id=team_id, channel_id=channel_id).exec()

    print(message.content)
    expected_texts = [
        "*create*",
        "*command_name*",
        "*pick-list*",
        "*label*",
        "*self-exclude*",
    ]
    for expected_text in expected_texts:
        assert expected_text in message.content
    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.HIDDEN


def test_help_with_given_custom_command(client):
    text = "test_help"
    Command.create(
        name="test_help",
        channel_id=channel_id,
        label="my fancy label",
        pick_list=["1", "2"],
        self_exclude=True,
        only_active_users=False,
        created_by_user_id="4321",
    )
    message = HelpCommand(text=text, team_id=team_id, channel_id=channel_id).exec()

    expected_texts = [
        "test_help",
        "• Message: ",
        "• Pick list: ",
        "• User using the slash command excluded.",
    ]
    for expected_text in expected_texts:
        assert expected_text in message.content
    assert message.status == MessageStatus.INFO
    assert message.visibility == MessageVisibility.HIDDEN

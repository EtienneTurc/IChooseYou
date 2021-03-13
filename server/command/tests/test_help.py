from server.command.help import HelpCommand
from server.orm.command import Command
from server.slack.message_status import MessageStatus, MessageVisibility
from server.tests.test_app import *  # noqa: F401, F403

channel_id = "1234"


def test_help_with_no_commands(client):
    text = ""
    Command.create("test_help", channel_id, "my fancy label", ["1", "2"], True, "4321")
    message, message_status, message_visibility = HelpCommand(text, channel_id).exec()

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
        assert expected_text in message
    assert message_status == MessageStatus.INFO
    assert message_visibility == MessageVisibility.HIDDEN


def test_help_with_given_known_command(client):
    text = "create"
    message, message_status, message_visibility = HelpCommand(text, channel_id).exec()

    expected_texts = [
        "*create*",
        "*commandName*",
        "*pickList*",
        "*label*",
        "*selfExclude*",
    ]
    for expected_text in expected_texts:
        assert expected_text in message
    assert message_status == MessageStatus.INFO
    assert message_visibility == MessageVisibility.HIDDEN


def test_help_with_given_custom_command(client):
    text = "test_help"
    Command.create("test_help", channel_id, "my fancy label", ["1", "2"], True, "4321")
    message, message_status, message_visibility = HelpCommand(text, channel_id).exec()

    expected_texts = [
        "test_help",
        "• Message: ",
        "• Pick list: ",
        "• User using the slash command excluded.",
    ]
    for expected_text in expected_texts:
        assert expected_text in message
    assert message_status == MessageStatus.INFO
    assert message_visibility == MessageVisibility.HIDDEN

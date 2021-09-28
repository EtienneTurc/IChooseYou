import pytest

from server.service.command.custom.helper import create_custom_command_label


@pytest.mark.parametrize(
    "command_label, additional_text, expected_label",
    [
        (
            "",
            "",
            "",
        ),
        (
            "",
            "world",
            "world",
        ),
        (
            "Hello",
            "",
            "Hello",
        ),
        (
            "Hello",
            "world",
            "Hello world",
        ),
        (
            "Hello",
            "world is wonderful",
            "Hello world is wonderful",
        ),
        (
            "I am here",
            "",
            "I am here",
        ),
    ],
)
def test_create_custom_command_label(command_label, additional_text, expected_label):
    assert create_custom_command_label(command_label, additional_text) == expected_label

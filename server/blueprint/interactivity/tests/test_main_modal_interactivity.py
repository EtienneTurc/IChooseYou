import json

from flask import current_app

from server.blueprint.event.tests.conftest import *  # noqa: F401, F403
from server.blueprint.interactivity.action import BlueprintInteractivityAction
from server.blueprint.interactivity.tests.helper import call_webhook
from server.service.slack.modal.enum import (SlackMainModalOverflowActionId,
                                             SlackModalSubmitAction)
from server.service.slack.tests.monkey_patch import *  # noqa: F401, F403
from server.tests.test_app import *  # noqa: F401, F403


def test_interactivity_main_modal_select_command(client, test_command):
    response, slack_message = call_webhook(
        client,
        action_id=BlueprintInteractivityAction.MAIN_MODAL_SELECT_COMMAND.value,
        action_value=str(test_command._id),
    )
    assert response.status_code == 200
    assert "'type': 'modal'" in slack_message
    assert (
        f"'callback_id': '{SlackModalSubmitAction.RUN_CUSTOM_COMMAND.value}.{test_command._id}'"  # noqa E501
        in slack_message
    )
    assert (
        "'title': {'type': 'plain_text', 'text': " + f"'{test_command.name}'"
        in slack_message
    )


def test_interactivity_main_modal_create_new_command(client):
    response, slack_message = call_webhook(
        client,
        action_id=BlueprintInteractivityAction.MAIN_MODAL_CREATE_NEW_COMMAND.value,
        view_metadata={"channel_id": "1234"},
    )
    assert response.status_code == 200
    assert "'type': 'modal'" in slack_message
    assert (
        f"'callback_id': '{SlackModalSubmitAction.CREATE_COMMAND.value}'"
        in slack_message
    )
    assert (
        "'private_metadata': '"
        + json.dumps(
            {
                "channel_id": "1234",
                "command_name": None,
                "pick_list": None,
                "user_select_enabled": True,
            }
        )
    ) in slack_message


def test_interactivity_main_modal_update_command(client, test_command):
    response, slack_message = call_webhook(
        client,
        action_id=BlueprintInteractivityAction.MAIN_MODAL_UPDATE_COMMAND.value,
        action_value=f"{SlackMainModalOverflowActionId.UPDATE_COMMAND.value}.{test_command._id}",  # noqa E501
        view_metadata={"channel_id": "1234"},
    )
    assert response.status_code == 200
    assert "'type': 'modal'" in slack_message
    assert (
        f"'callback_id': '{SlackModalSubmitAction.UPDATE_COMMAND.value}'"
        in slack_message
    )
    assert (
        "'private_metadata': '"
        + json.dumps(
            {
                "channel_id": "1234",
                "command_name": test_command.name,
                "pick_list": test_command.pick_list,
                "user_select_enabled": True,
            }
        )
    ) in slack_message


def test_interactivity_main_modal_run_instant_command(client):
    response, slack_message = call_webhook(
        client,
        action_id=BlueprintInteractivityAction.MAIN_MODAL_RUN_INSTANT_COMMAND.value,
        view_metadata={"channel_id": "1234"},
    )
    assert response.status_code == 200
    assert "'type': 'modal'" in slack_message
    assert (
        f"'callback_id': '{SlackModalSubmitAction.RUN_INSTANT_COMMAND.value}'"
        in slack_message
    )
    assert (
        "'private_metadata': '"
        + json.dumps(
            {
                "channel_id": "1234",
                "pick_list": None,
                "user_select_enabled": True,
            }
        )
    ) in slack_message


def test_interactivity_main_modal_delete_command(client, test_command):
    response, slack_message = call_webhook(
        client,
        action_id=BlueprintInteractivityAction.MAIN_MODAL_DELETE_COMMAND.value,
        action_value=f"{SlackMainModalOverflowActionId.DELETE_COMMAND.value}.{test_command._id}",  # noqa E501
        view_metadata={"channel_id": "1234"},
    )
    assert response.status_code == 200
    assert f"Command {test_command.name} successfully deleted." in slack_message
    assert "'type': 'modal'" in slack_message
    assert (
        "'title': {'type': 'plain_text', 'text': "
        + f"'{current_app.config['APP_NAME']}'"
        in slack_message
    )

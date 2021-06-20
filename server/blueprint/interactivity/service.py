import threading
from flask import current_app


from server.blueprint.interactivity.action import Action
from server.blueprint.interactivity.helper import (
    format_payload_for_slash_command,
    format_payload_for_message_delete,
    assert_message_can_be_delete,
)
from server.blueprint.slash_command.service import process_slash_command
from server.service.error.decorator import handle_error
from server.service.flask.decorator import make_context
from server.service.slack.sdk_wrapper import delete_message_in_channel


def proccess_interactivity(payload):
    action = payload.get("callback_id") or payload.get("actions")[0].get("action_id")
    if action == Action.RESUBMIT_COMMAND.value:
        body = format_payload_for_slash_command(payload)
        return process_slash_command(body)
    elif action == Action.DELETE_MESSAGE.value:
        body = format_payload_for_message_delete(payload)
        thread = threading.Thread(
            target=delete_message,
            args=(current_app._get_current_object(),),
            kwargs=body,
        )
        thread.start()
        if current_app.config["WAIT_FOR_THREAD_BEFORE_RETURN"]:
            thread.join()
        return ""
    return "Action not handled"


@make_context
@handle_error
def delete_message(
    *, team_id: str, channel_id: str, ts: str, user_id: str, text: str, **kwargs
) -> None:
    assert_message_can_be_delete(text, user_id)
    delete_message_in_channel(team_id, channel_id, ts)

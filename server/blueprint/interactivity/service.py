from server.blueprint.interactivity.action import Action
from server.blueprint.interactivity.helper import format_payload_for_slash_command
from server.blueprint.slash_command.service import process_slash_command


def proccess_interactivity(payload):
    action = payload.get("actions")[0].get("action_id")
    if action == Action.RESUBMIT_COMMAND.value:
        body = format_payload_for_slash_command(payload)
        return process_slash_command(body)
    return "Action not handled"

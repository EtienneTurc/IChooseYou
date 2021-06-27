from server.blueprint.event.helper import format_payload_to_complete_workflow
from server.blueprint.event.type import EventType
from server.blueprint.slash_command.service import resolve_command
from server.service.error.decorator import handle_workflow_error
from server.service.flask.decorator import make_context
from server.service.helper.thread import launch_function_in_thread
from server.service.slack.sdk_wrapper import complete_workflow, send_message_to_channel
from server.service.slack.workflow import OutputVariable


def process_event(payload):
    event_type = payload.get("event").get("type")
    event_types = [event_type]

    if EventType.WORKFLOW_STEP_EXECUTE.value in event_types:
        body = format_payload_to_complete_workflow(payload)
        launch_function_in_thread(process_workflow_step, body)

        return ""
    return "Event not handled"


@make_context
@handle_workflow_error
def process_workflow_step(
    *,
    workflow_step_execute_id: str,
    team_id: str,
    channel: dict[str, str],
    user: dict[str, str],
    command_name: str,
    text: str,
    send_to_slack: bool,
    **kwargs,
) -> None:
    message, selected_item = resolve_command(
        team_id=team_id,
        channel=channel,
        user=user,
        command_name=command_name,
        text=text,
    )

    if send_to_slack:
        send_message_to_channel(message, channel["id"], team_id, user_id=user["id"])

    outputs = {
        OutputVariable.SELECTED_ITEM.value: selected_item,
        OutputVariable.SELECTION_MESSAGE.value: message.content,
    }
    complete_workflow(workflow_step_execute_id, outputs, team_id)

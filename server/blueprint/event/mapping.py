from server.blueprint.event.action import BlueprintEventAction
from server.service.error.handler.workflow import workflow_error_handler
from server.service.formatter.event import format_event_complete_workflow_payload
from server.service.slack.responder.message import send_message_and_complete_workflow
from server.service.slack.workflow.processor import workflow_step_execute_processor
from server.service.tpr.enum import DataFlow

BLUEPRINT_EVENT_ACTION_TO_DATA_FLOW = {
    BlueprintEventAction.WORKFLOW_STEP_EXECUTE.value: DataFlow(
        formatter=format_event_complete_workflow_payload,
        processor=workflow_step_execute_processor,
        responder=send_message_and_complete_workflow,
        error_handler=workflow_error_handler,
    ),
}

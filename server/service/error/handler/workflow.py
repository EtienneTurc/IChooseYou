import traceback

from server.service.slack.response.api_response import (
    failed_worklow,
)


def workflow_error_handler(
    error: Exception, *, workflow_step_execute_id: str, team_id: str, **kwargs
) -> None:
    traceback.print_exc()  # Print stacktrace

    return failed_worklow(
        message=error.message,
        workflow_step_execute_id=workflow_step_execute_id,
        team_id=team_id,
    )

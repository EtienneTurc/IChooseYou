from server.service.tpr.mapping import (
    BLUEPRINT_ACTION_TO_DATA_FLOW,
    RESPONSE_TYPE_TO_RESPONSE_ACTION,
)
from server.service.helper.thread import launch_function_in_thread
from server.service.flask.decorator import make_context
from server.service.error.decorator import tpr_handle_error
from server.service.tpr.response_format import Response


@tpr_handle_error
def transform_process_respond(
    blueprint_action: str, payload: dict[str, any], run_in_thread=True
) -> str:
    data = BLUEPRINT_ACTION_TO_DATA_FLOW[blueprint_action].formatter(payload)

    return run_processor(
        BLUEPRINT_ACTION_TO_DATA_FLOW[blueprint_action].processor,
        data,
        run_in_thread,
    )


def run_processor(processor: any, data: dict[str, any], run_in_thread: bool) -> str:
    if not run_in_thread:
        response = processor(**data)
        return RESPONSE_TYPE_TO_RESPONSE_ACTION[response.type](response, data)

    launch_function_in_thread(
        run_processor_in_thread, {"processor": processor, "data": data}
    )
    return ""


@make_context
@tpr_handle_error
def run_processor_in_thread(*, processor: any, data: dict[str, any]) -> str:
    response: Response = processor(**data)
    return RESPONSE_TYPE_TO_RESPONSE_ACTION[response.type](**response.data, **data)

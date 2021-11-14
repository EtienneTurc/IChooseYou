from server.service.error.decorator import tpr_handle_error
from server.service.flask.decorator import make_context
from server.service.helper.thread import launch_function_in_thread
from server.service.tpr.mapping import BLUEPRINT_ACTION_TO_DATA_FLOW


def get_tpr_error_handler_func(blueprint_action: str, *args, **kwargs) -> any:
    return BLUEPRINT_ACTION_TO_DATA_FLOW[blueprint_action].error_handler


def get_tpr_error_handler_in_thread_func(*args, **kwargs) -> any:
    return kwargs.get("error_handler")


@tpr_handle_error(get_tpr_error_handler_func)
def transform_process_respond(blueprint_action: str, payload: dict[str, any]) -> str:
    data = BLUEPRINT_ACTION_TO_DATA_FLOW[blueprint_action].formatter(payload)

    launch_function_in_thread(
        run_processor_and_respond_in_thread,
        {
            "processor": BLUEPRINT_ACTION_TO_DATA_FLOW[blueprint_action].processor,
            "responder": BLUEPRINT_ACTION_TO_DATA_FLOW[blueprint_action].responder,
            "error_handler": BLUEPRINT_ACTION_TO_DATA_FLOW[
                blueprint_action
            ].error_handler,
            "data": data,
        },
    )

    fast_responder = BLUEPRINT_ACTION_TO_DATA_FLOW[blueprint_action].fast_responder
    if fast_responder:
        return fast_responder(**data)

    return ""


@make_context
@tpr_handle_error(get_tpr_error_handler_in_thread_func)
def run_processor_and_respond_in_thread(
    *, processor: any, responder: any, data: dict[str, any], **kwargs
) -> None:
    processor_response_data = processor(**data)
    responder(**{**data, **processor_response_data})

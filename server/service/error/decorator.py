from flask import request


def tpr_handle_error(get_error_handler_func):
    def tpr_handle_error_decorator(func, *args, **kwargs):
        def tpr_handle_error_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                req = kwargs.get("request") or {
                    "route": request.path,
                    "method": request.method,
                    "payload": kwargs["request_payload"],
                }

                return get_error_handler_func(*args, **kwargs)(
                    error, request=req, **kwargs.get("data")
                )

        return tpr_handle_error_wrapper

    return tpr_handle_error_decorator

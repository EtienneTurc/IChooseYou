def tpr_handle_error(get_error_handler_func):
    def tpr_handle_error_decorator(func):
        def tpr_handle_error_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                return get_error_handler_func(*args, **kwargs)(
                    error, **kwargs.get("data")
                )

        return tpr_handle_error_wrapper

    return tpr_handle_error_decorator

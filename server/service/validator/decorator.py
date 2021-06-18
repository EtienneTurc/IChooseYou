def validate_schema(schema):
    def validate_decorator(func):
        def validate_wrapper(*args, **kwargs):
            schema().load(kwargs)
            return func(*args, **kwargs)

        return validate_wrapper

    return validate_decorator

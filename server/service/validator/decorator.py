def validate_schema(schema):
    def validate_decorator(func):
        def validate_wrapper(*args, **kwargs):
            data = schema().load(kwargs)
            return func(*args, **data)

        return validate_wrapper

    return validate_decorator

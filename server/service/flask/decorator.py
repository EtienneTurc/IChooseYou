def make_context(func):
    def make_context_wrapper(app, *args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)

    return make_context_wrapper

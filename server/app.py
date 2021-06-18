from flask import Flask

from server.config import CONFIG


def create_app(config_name="prod"):
    app = Flask(__name__)

    # Configure app
    app.config.from_object(CONFIG[config_name]())

    # Connect to DB
    from pymodm import connect

    connect(app.config["DATABASE_URI"])

    # Add blueprints
    from server.blueprint.authentication.blueprint import api as authentication_api
    from server.blueprint.interactivity.blueprint import api as interactivity_api
    from server.blueprint.slash_command.blueprint import api as slash_command_api

    app.register_blueprint(authentication_api)
    app.register_blueprint(interactivity_api)
    app.register_blueprint(slash_command_api)

    return app

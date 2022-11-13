import logging

from flask import Flask

from server.config import CONFIG


def create_app(config_name="prod"):
    app = Flask(__name__)

    # Configure app
    app.config.from_object(CONFIG[config_name]())

    logging.basicConfig(
        format="%(asctime)s - [%(levelname)8s] %(message)s",
        level=logging.ERROR,
        force=True,
    )

    # Connect to DB
    from pymodm import connect

    connect(app.config["DATABASE_URI"])

    # Add blueprints
    from server.blueprint.authentication.blueprint import api as authentication_api
    from server.blueprint.chart.blueprint import api as chart_api
    from server.blueprint.event.blueprint import api as event_api
    from server.blueprint.interactivity.blueprint import api as interactivity_api
    from server.blueprint.slash_command.blueprint import api as slash_command_api

    app.register_blueprint(authentication_api)
    app.register_blueprint(interactivity_api)
    app.register_blueprint(slash_command_api)
    app.register_blueprint(event_api)
    app.register_blueprint(chart_api)

    return app

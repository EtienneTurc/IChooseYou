from flask import Flask

from server.config import CONFIG


def create_app(config_name):
    app = Flask(__name__)

    # Configure app
    app.config.from_object(CONFIG[config_name]())

    # Connect to DB
    from pymodm import connect

    connect(app.config["DATABASE_URI"])

    # Add blueprints
    from server.blueprint.slack_webhook import slack_webhook

    app.register_blueprint(slack_webhook)

    return app

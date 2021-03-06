from server.app import create_app
import pytest


@pytest.fixture()
def client():
    flask_app = create_app("test")

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

    from pymongo import MongoClient

    mongo_client = MongoClient(flask_app.config["DATABASE_URI"])
    mongo_client.drop_database(flask_app.config["DATABASE_URI"].split("/")[-1])

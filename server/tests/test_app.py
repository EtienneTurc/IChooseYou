import pytest

from server.app import create_app


@pytest.fixture()
def client():
    flask_app = create_app("test")

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

    clear_db(flask_app.config["DATABASE_URI"])


def clear_db(database_uri):
    from pymongo import MongoClient

    mongo_client = MongoClient(database_uri)
    mongo_client.drop_database(database_uri.split("/")[-1])

import pytest

from app import create_app
from app.config import TestingConfig
from app.database import db
from app.models.user_model import UserModel


@pytest.fixture(scope="session")  # default scope is function --> so it starts and end after each and every function.
#  now it is for session so for all tests in one run
def app():
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        db.create_all()  # before returning app for testing
        yield app
        db.drop_all()  # thanks to yield we can clean up all resources now - after testing


@pytest.fixture(scope="session")
def client(app):
    app.testing = True
    return app.test_client()
    # app.test_client() is used to create a test client for the application.
    # This test client simulates requests to the application without having to run the server.
    # It provides a way to interact with the app's endpoints, making it easier to test various routes,
    # their responses, and behavior.


@pytest.fixture()
def get_headers():
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    return headers


@pytest.fixture()
def new_user():
    user = UserModel(user_login='mati', user_password='abc')
    return user

# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner() # used to provide arguments in cli

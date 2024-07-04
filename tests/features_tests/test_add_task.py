import json

import pytest
from pytest_bdd import scenarios, given, when, then, scenario
from app.models.task_model import TaskModel
from app.database import db


# Load the feature file
@scenario('../../features/add_task.feature', 'Successfully add a new task')
def test_adding():
    pass


@pytest.fixture
@given('task payload')
def task_payload():
    return {
        'name': 'first task'
    }


@pytest.fixture()
@when('the client posts the payload to "/tasks/add"')
def post_task(client, get_headers, task_payload):
    # Create a mock task instance with the expected data
    response = client.post('/tasks/add', data=json.dumps(task_payload),
                           headers=get_headers)  # dumps used for converting inside app and jsonify used for response
    return response


@then('the response status code should be 200')
def check_status_code(post_task):
    assert post_task.status_code == 200


@then('the response should contain message "Task added"')
def check_response_data(post_task):
    response_data = post_task.get_json()
    assert response_data['message'] == "Task added"

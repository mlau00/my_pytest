import json
import uuid
import pytest
import mock

from app import models
from app.database import db
from app.models.task_model import TaskModel
from app.models.user_model import UserModel


def test_add_task(client, get_headers):
    """
    GIVEN endpoint to create task with name 'first task'
    WHEN task is added to db
    THEN verify response status code and return message - 'Task added'
    """
    data = {
        'name': 'first task'
    }
    response = client.post('/tasks/add', data=json.dumps(data),
                           headers=get_headers)  # dumps used for converting inside app and jsonify used for response
    res_data = response.get_json()
    assert response.status_code == 200
    assert res_data['message'] == 'Task added'


# def test_add_task(client, get_headers, mocker):
#     mock_data = {
#         "body": [],
#         "message": "Task added",
#         "status": 200
#     }
#
#     data = {
#         'name': 'first task'
#     }
#
#     # Create a mock response object with a .json() method that returns the mock data
#
#     mock_response = mocker.MagicMock()
#     mock_response.json.return_value = mock_data
#
#     # Patch 'requests.post' to return the mock response
#     mocker.patch("requests.post", return_value=mock_response)
#
#     # Call the function
#     result = client.post('/tasks/add', data=json.dumps(data), headers=get_headers)
#     res_data = result.get_json()
#
#     # Assertions to check if the returned data is as expected
#     assert res_data == mock_data
#     # assert isinstance(res_data, dict)
#     assert res_data["message"] == "Task added"

def test_add_task_with_mock(client, mocker):
    mock_data = {
        'name': 'first task'
    }

    # Create a mock task instance with the expected data
    mock_task = TaskModel(name=mock_data['name'])
    mock_task.id = 1  # Manually set the ID since it won't be auto-incremented in a mock

    # Mock the add and commit methods of the SQLAlchemy session
    mocker.patch('app.database.db.session.add')
    mocker.patch('app.database.db.session.commit')

    # Mock the query to return our mock_task when querying by ID
    mocker.patch('app.database.db.session.query',
                 return_value=mocker.MagicMock(filter_by=mocker.MagicMock(first=mock_task)))

    # Call the function
    response = client.post('/tasks/add', data=json.dumps(mock_data), headers={'Content-Type': 'application/json'})

    assert response.status_code == 200

    # Ensure db.session.add and db.session.commit were called once each
    db.session.add.assert_called_once()
    db.session.commit.assert_called_once()


def test_show_all_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert data['body'][0]['name'] == 'first task'
    assert data['message'] == 'Lista zadań'


def test_update_task(client, get_headers):
    data = {
        'id': 1,
        'name': 'second task'
    }

    response = client.post('/tasks/update', data=json.dumps(data), headers=get_headers)
    res_data = response.get_json()
    assert response.status_code == 200
    assert res_data['message'] == 'Zadanie zmienione'
    assert res_data['body']['name'] == 'second task'


def test_delete_task(client, get_headers):
    data = {
        'id': 1
    }

    response = client.post('/tasks/delete', data=json.dumps(data), headers=get_headers)
    res_data = response.get_json()

    assert response.status_code == 200
    assert res_data['body'] == True
    assert res_data['message'] == 'Zadanie usunięte'


def test_create_user(client, get_headers):
    data = {
        'login': 'a',
        'password': 'b'
    }

    response = client.post('/users/create', data=json.dumps(data), headers=get_headers)
    res_data = response.get_json()

    assert response.status_code == 200
    assert res_data['message'] == 'Użytkownik utworzony', 'Błędny message'
    assert res_data['body']['user_login'] == 'a'
    res_uuid = res_data['body']['user_id']
    print(res_uuid)
    print(uuid.UUID(res_uuid))
    assert res_uuid == str(uuid.UUID(res_uuid))


def test_login_user(client, get_headers):
    data = {
        'login': 'a',
        'password': 'b'
    }

    response = client.post('/users/login', data=json.dumps(data), headers=get_headers)
    res_data = response.get_json()

    assert response.status_code == 200
    assert res_data['message'] == 'Zalogowany', 'Błędny message'
    assert res_data['body']['user_login'] == 'a'
    res_uuid = res_data['body']['user_id']
    print(res_uuid)
    print(uuid.UUID(res_uuid))
    assert res_uuid == str(uuid.UUID(res_uuid))


def test_login_user_with_incorrect_credentials(client, get_headers):
    data = {
        'login': 'a',
        'password': 'c'
    }

    response = client.post('/users/login', data=json.dumps(data), headers=get_headers)
    res_data = response.get_json()

    assert res_data['message'] == 'Błędny użytkownik'
    assert response.status_code == 404

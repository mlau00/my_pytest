import json
import uuid

from app.models.task_model import TaskModel
from app.models.user_model import UserModel


def test_add_task(client, get_headers):
    data = {
        'name': 'first task'
    }
    response = client.post('/tasks/add', data=json.dumps(data),
                           headers=get_headers)  # dumps used for converting inside app and jsonify used for response
    res_data = response.get_json()
    assert response.status_code == 200
    assert res_data['message'] == 'Task added'


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

import uuid

from app.models.task_model import TaskModel
from app.models.user_model import UserModel


def test_task_model(client):
    """
    GIVEN a task with name 'task1'
    WHEN the task is created
    THEN check task name ('task1') and serialize method to return a correct object
    """
    task = TaskModel(name='task1')
    print(task.serialize())
    assert task.name == 'task1'
    assert task.serialize()['name'] == 'task1'


def test_user_model():
    """
    GIVEN a user with login 'aa' and password 'bb'
    WHEN the user is created
    THEN the user login is correct -> 'aa'
    """
    user = UserModel(user_login='aa', user_password='bb')
    print(user.serialize())
    assert user.user_login == 'aa'


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model from fixture
    WHEN a new User is created
    THEN check the login, id and session id fields are defined correctly
    """
    assert new_user.user_login == 'mati'
    assert new_user.user_id == str(uuid.UUID(new_user.user_id))
    assert new_user.user_session_id == str(uuid.UUID(new_user.user_session_id))

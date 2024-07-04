class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo_tasks_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_todo_tasks_db'
    TESTING = True

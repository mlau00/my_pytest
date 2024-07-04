from flask import Flask, jsonify, request
import os

from flask_cors import CORS

from app.config import Config
from app.database import db
from app.models.response_body import ResponseBody
from app.models.task_model import TaskModel
from app.models.user_model import UserModel


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    os.environ['FLASK_DEBUG'] = 'True'
    app.config.from_object(config_class)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return jsonify({'hello': 'world'})

    @app.route('/tasks')
    def show_all_tasks():
        # query = "SELECT * FROM tasks"
        # proxy_results = connection.execute(text(query))
        # results = proxy_results.fetchall()
        tasks = db.session.query(TaskModel).all()
        tasks_json = []

        for task in tasks:
            tasks_json.append(task.serialize())

        return jsonify(
            ResponseBody(200, "Lista zadań", tasks_json).serialize()
        ), 200

    @app.route('/tasks/add', methods=['POST'])
    def add_task():
        if request.method == 'POST':
            data = request.get_json()
            task_name = data['name']

            task = TaskModel(name=task_name)
            db.session.add(task)
            db.session.commit()
            print(task.id)

        return jsonify(ResponseBody(200, 'Task added', []).serialize()), 200

    @app.route('/tasks/delete', methods=['POST'])
    def delete_task():
        if request.method == 'POST':
            data = request.get_json()
            task_id = data['id']

            db.session.delete(TaskModel.query.filter_by(id=task_id).first())

            db.session.commit()

            return jsonify(ResponseBody(200, "Zadanie usunięte", True).serialize()), 200

    @app.route('/tasks/update', methods=['POST'])
    def update_task():
        if request.method == 'POST':
            data = request.get_json()
            task_id = data['id']
            task_name = data['name']

            task = db.session.query(TaskModel).filter_by(id=task_id).first()
            task.name = task_name
            updated_task = task.serialize()
            db.session.commit()
            return jsonify(ResponseBody(200, "Zadanie zmienione", updated_task).serialize()), 200

    @app.route('/users/login', methods=['POST'])
    def login_user():
        if request.method == 'POST':
            data = request.get_json()
            login = data['login']
            password = data['password']

            user = db.session.query(UserModel).filter_by(user_login=login, user_password=password).first()

            if user is None:
                return ResponseBody(404, 'Błędny użytkownik', None).serialize(), 404

            print(user.serialize())
            return jsonify(ResponseBody(200, "Zalogowany", user.serialize()).serialize()), 200

    @app.route('/users/create', methods=['POST'])
    def create_user():
        if request.method == 'POST':
            data = request.get_json()
            login = data['login']
            password = data['password']
            user = UserModel(user_login=login, user_password=password)
            db.session.add(user)
            db.session.commit()
            print(user.user_id)

            return jsonify(ResponseBody(200, "Użytkownik utworzony", user.serialize()).serialize()), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', '8080')), debug=True)

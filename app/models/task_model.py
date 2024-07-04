from sqlalchemy import Integer, String

from ..database import db


class TaskModel(db.Model):
    __tablename__ = 'tasks'
    id = db.Column('id', Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', String(36))

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

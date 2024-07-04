import uuid

from ..database import db


class UserModel(db.Model):
    __tablename__ = 'users'
    # user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # user_login = db.Column(db.String(36))
    # user_password = db.Column(db.String(36))
    # user_session_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()))

    user_id = db.Column(db.String(36), primary_key=True)
    user_login = db.Column(db.String(36))
    user_password = db.Column(db.String(36))
    user_session_id = db.Column(db.String(36))

    def __init__(self, user_login, user_password):
        self.user_id = str(uuid.uuid4())
        self.user_login = user_login
        self.user_password = user_password
        self.user_session_id = str(uuid.uuid4())

    # db.Model without init!!
    def serialize(self):
        return {
            'user_id': self.user_id,
            'user_login': self.user_login,
            'user_session_id': self.user_session_id
        }

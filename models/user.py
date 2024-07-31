from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    User model class for storing user related details.
    It is mapping id, username, password to the user table.
    """
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), nullable=False, unique=True)
    password: str = db.Column(db.String(80), nullable=False)
    role: str = db.Column(db.String(80), nullable=False, default='user')
    
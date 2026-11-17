from ..extensions import db
import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    display_name = db.Column(db.String, nullable=True)
    role = db.Column(db.String, nullable=False, server_default='user')

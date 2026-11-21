from ..extensions import db

class Province(db.Model):
    __tablename__ = 'provinces'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    current_turn = db.Column(db.String, nullable=False, server_default='1')
    difficulty = db.Column(db.String, nullable=False, server_default='Medium')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



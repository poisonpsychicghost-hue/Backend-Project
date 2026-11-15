from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from .models import User
from ..extensions import db

user_route_bp = Blueprint("user", __name__, url_prefix="/user")

def register_user():
    if not request.is_json:
        return jsonify({"code": "Bad_Request", "message": "Request Body must be JSON"}), 400
    data = request.get_json()
    missing_fields = []
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    display_name = data.get("display_name")
    if username is None or username.strip() == '':
        missing_fields.append('username')
    if password is None or password.strip() == '':
        missing_fields.append('password')
    if len(missing_fields) > 0:
        return jsonify({"code": "Bad Request", "message": f"Missing Required Fields: ({missing_fields})"}), 400
    field = None
    if len(username) < 4 or len(username) > 32:
        field = 'username'
    if len(password) < 8 or len(password) > 64:
        field = 'password'
    if email is not None and email != "":
        if len(email) < 8 or len(email) > 128 or "@" not in email:
            field = 'email'
    if display_name is not None and display_name != "":
        if len(display_name) < 4 or len(display_name) > 32:
            field = 'display_name'
    if field:
        return jsonify( {"code": "Bad_Request", "message": f"Field ({field}) Invalid. Please review the User FAQ"}), 400

    existing = User.query.filter_by(username=username).first()
    if existing is not None:
        return jsonify({"code": "Username_Taken", "message": "Username already exists. Please try again with a new username"}), 409

    password_hash = generate_password_hash(password)

    user = User(username=username, email=email, password_hash=password_hash, display_name=display_name)
    db.session.add(user)
    db.session.commit()

    print("Register route called")
    return_body = {"message": "User Creation Successful", "username": user.username, "email": user.email, "id": user.id, "display_name": user.display_name, "created_at": user.created_at}

    return jsonify(return_body), 201

user_route_bp.add_url_rule(
    "/register",
    view_func=register_user,
    methods=["POST"]
)

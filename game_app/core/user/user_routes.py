from flask import Blueprint, request, jsonify, current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from ..extensions import db
from .auth_decorators import require_auth_token
import jwt
import datetime

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

def user_login():
    if not request.is_json:
        return jsonify({"code": "Bad_Request", "message": "Request Body must be JSON."}), 400
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if (username is None or username == "") or (password is None or password == ""):
        return jsonify({"code": "Unauthorized", "message": "Invalid Credentials."}), 401
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"code": "Unauthorized", "message": "Invalid Credentials."}), 401
    if check_password_hash(user.password_hash, password) == False:
        return jsonify({"code": "Unauthorized", "message": "Invalid Credentials."}), 401

    expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=current_app.config["JWT_LIFETIME_HOURS"])
    payload = {
        'sub': str(user.id),
        'username': str(user.username),
        'role': user.role,
        'exp': expiry
    }
    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm="HS256"
    )

    response_body = {"username": user.username, "token": token, "message": f"Login OK. Token Expiry: ({expiry})"}
    return jsonify(response_body), 200

@require_auth_token
def user_profile_getter():
    user_id = g.user_id
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'code': 'Not Found', 'message': 'User Profile Not Found'}), 404

    body = {
        'id': user.id,
        'username': user.username,
        'created_at': user.created_at,
        'display_name': user.display_name,
        'email': user.email
    }

    return jsonify(body), 200

@require_auth_token
def user_profile_update():
    if not request.is_json:
        return jsonify({"code": "Bad_Request", "message": "Request Body must be JSON."}), 400
    data = request.get_json()
    user_id = g.user_id
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'code': 'Not Found', 'message': 'User Profile Not Found'}), 404
    if 'display_name' in data:
        display_name = data.get('display_name').strip()
        if len(display_name) < 4 or len(display_name) > 32:
            return jsonify({'code': 'Bad Request', 'message': 'Display Name must be between 4-32 Characters'}), 400
        user.display_name = display_name
    if 'email' in data:
        email = data.get('email').strip()
        if len(email) < 8 or len(email) > 128:
            return jsonify({'code': 'Bad Request', 'message': 'Email must be between 8 and 128 Characters'}), 400
        if '@' not in email:
            return jsonify({'code': 'Bad Request', 'message': 'Email must contain an "@" symbol.'}), 400
        user.email = email
    db.session.commit()
    user = User.query.filter_by(id=user_id).first()
    body = {
        'id': user.id,
        'username': user.username,
        'created_at': user.created_at,
        'display_name': user.display_name,
        'email': user.email
        }
    return jsonify(body), 200
    
    

user_route_bp.add_url_rule(
    "/register",
    view_func=register_user,
    methods=["POST"]
)

user_route_bp.add_url_rule(
    "/login",
    view_func=user_login,
    methods=["POST"]
)

user_route_bp.add_url_rule(
    '/me',
    view_func=user_profile_getter,
    methods=['GET']
)

user_route_bp.add_url_rule(
    '/me',
    view_func=user_profile_update,
    methods=["PATCH"]
)

from .auth_decorators import require_auth_token
from .models import User
from flask import Blueprint, g, jsonify

admin_route_bp = Blueprint('admin', __name__, url_prefix='/admin')

@require_auth_token
def get_system_check():
    is_admin = g.role == 'admin'
    if is_admin != True:
        return jsonify({'code': 'Forbidden', 'message': 'Admin Access Only.'}), 403

    users = User.query.all()

    user_list = []
    for user in users:
        current_user = {
            "username": user.username,
            "id": user.id,
            "role": user.role,
            'created_at': user.created_at
        }
        user_list.append(current_user)

    return jsonify({'user_list': user_list}), 200 

admin_route_bp.add_url_rule(
    "/system-check",
    view_func=get_system_check,
    methods=["GET"]
)

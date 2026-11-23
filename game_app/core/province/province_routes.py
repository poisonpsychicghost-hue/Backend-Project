from flask import Blueprint, request, jsonify, current_app, g
from .models import Province
from ..extensions import db
from ..user.auth_decorators import require_auth_token

province_route_bp = Blueprint('province', __name__, url_prefix='/province')

@require_auth_token
def create_province():
    if not request.is_json:
        return jsonify({'code': 'Bad Request', 'message': 'Request Body must be JSON'}), 400
    data = request.get_json()
    user_id = g.user_id
    missing_fields = []
    name = data.get('name')
    difficulty = data.get('difficulty')
    if name is None or name.strip() == '':
        return jsonify({'code': 'Bad Request', 'message': 'Province Name Required'}), 400
    if difficulty is None or difficulty.strip() == '':
        difficulty = 'medium'
    if difficulty.lower().strip() not in ['easy', 'medium', 'hard']:
        return jsonify({'code': 'Bad Request', 'message': 'Difficulty Setting Must Be ("easy", "medium", or "hard").'}), 400
    existing = Province.query.filter_by(name=name).first()
    if existing is not None:
        return jsonify({'code': 'Name Conflict', 'message': 'A Province with that name already exists.'}), 409

    province = Province(name=name, difficulty=difficulty, user_id=user_id)
    db.session.add(province)
    db.session.commit()

    return_body = {'message': 'Province Creation Successful', 'id': province.id, 'name': province.name, 'user_id': province.user_id, 'created_at': province.created_at, 'difficulty': province.difficulty, 'current_turn': province.current_turn}
    return jsonify(return_body), 201

@require_auth_token
def list_my_provinces():
    user_id = g.user_id
    provinces = Province.query.filter_by(user_id=user_id).all()
    return_list = []
    for province in provinces:
        item = {
            'id': province.id,
            'name': province.name,
            'created_at': province.created_at,
            'difficulty': province.difficulty,
            'current_turn': province.current_turn,

        }
        return_list.append(item)
    return jsonify({'message': f'List of Provinces for user {user_id}', 'province_list': return_list}), 200

province_route_bp.add_url_rule(
    '/create',
    view_func=create_province,
    methods=["POST"]
)

province_route_bp.add_url_rule(
    '/list',
    view_func=list_my_provinces,
    methods=['GET']
)
    
    
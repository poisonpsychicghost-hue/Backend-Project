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
    page = 1
    per_page = 10
    try:
        if request.args.get('page'):
            if int(request.args.get('page')) >= 1:
                page = int(request.args.get('page'))
        if request.args.get('per_page'):
            if int(request.args.get('per_page')) >= 1 and int(request.args.get('per_page')) <= 25:
                per_page = int(request.args.get('per_page'))
    except ValueError:
        page = 1
        per_page = 10
    query = Province.query.filter_by(user_id=user_id).order_by(Province.id)
    provinces_page = query.paginate(page=page, per_page=per_page, error_out=False)
    return_list = []
    for province in provinces_page.items:
        item = {
            'id': province.id,
            'name': province.name,
            'created_at': province.created_at,
            'difficulty': province.difficulty,
            'current_turn': province.current_turn,

        }
        return_list.append(item)
    return jsonify({'message': f'List of Provinces for user {user_id}', 'page': page, 'per_page': per_page, 'total': provinces_page.total, 'pages': provinces_page.pages, 'province_list': return_list}), 200

@require_auth_token
def province_by_id(id):


    province = Province.query.filter_by(id=id).first()
    if province is None:
        return jsonify({'code': 'Not Found', 'message': 'Province Not Found'}), 404

    is_owner = g.user_id == province.user_id
    is_admin = g.role == 'admin'

    if request.method == 'GET':
        if not (is_owner or is_admin):
            return jsonify({'code': 'Forbidden', 'message': 'You do not have access to this Province'}), 403


        return_body = {
            'id': province.id,
            'name': province.name,
            'current_turn': province.current_turn,
            'created_at': province.created_at,
            'difficulty': province.difficulty,
            'owner': province.owner.username
        }
        return jsonify(return_body), 200
    
    if request.method == 'PATCH':
        if not request.is_json:
            return jsonify({'code': 'Bad Request', 'message': 'Request Body must be JSON'}), 400
        if not (is_owner or is_admin):
            return jsonify({'code': 'Forbidden', 'message': 'You do not have access to this Province'}), 403
        data = request.get_json()
        if data.get('name') is not None:
            if data.get('name').strip() != '':
                province.name = data.get('name')
        if data.get('difficulty') is not None:
            if data.get('difficulty').strip() not in ['easy', 'medium', 'hard']:
                return jsonify({'code': 'Bad Request', 'message': 'Difficulty must be ("easy", "medium", or "hard").'}), 400
            if data.get('difficulty').strip != '':
                province.difficulty = data.get('difficulty')
        if is_admin:
            if data.get('current_turn') is not None:
                province.current_turn = str(data.get('current_turn'))
        db.session.commit()
        return_body = {
            'id': province.id,
            'name': province.name,                
            'current_turn': province.current_turn,
            'difficulty': province.difficulty                        
        }
        return jsonify(return_body), 200

    if request.method == 'DELETE':
        if not (is_owner or is_admin):
            return jsonify({'code': 'Forbidden', 'message': 'You do not have access to this Province'}), 403
        p_id = province.id
        db.session.delete(province)
        db.session.commit()
        return jsonify({'code': 'Deleted', 'message': f'Province {p_id} Deleted Successfully'}), 200

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

province_route_bp.add_url_rule(
    '/<int:id>',
    view_func=province_by_id,
    methods=['GET', 'PATCH', 'DELETE']
)    

from flask import jsonify, g, current_app, request
from functools import wraps
import jwt

def require_auth_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'code': 'Unauthorized', 'message': 'No Authorization Header'}), 401

        token = auth_header[len("Bearer "):].strip()

        try:
            claims = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
            g.role = claims.get('role')
            try:
                g.user_id = int(claims.get('sub'))
            except (TypeError, ValueError):
                return jsonify({'code': 'Unauthorized', 'message': 'Invalid Token.'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'code': 'Expired_Token', 'message': 'Token Has Expired. Please Re-Login and Try Again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'code': 'Unauthorized', 'message': 'Invalid Token.'}), 401

        return f(*args, **kwargs)
    return wrapper


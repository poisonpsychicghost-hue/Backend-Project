from flask import jsonify

def make_error_response(code_str, message, status_code):
    return jsonify({'code': code_str, 'message': message}), status_code

def bad_request_handler(err):
    return make_error_response('Bad Request', 'Invalid Request', 400)

def unauthorized_handler(err):
    return make_error_response('Unauthorized', 'Unauthorized Request', 401)

def forbidden_handler(err):
    return make_error_response('Forbidden', 'You do not have permission to perform this action', 403)

def not_found_handler(err):
    return make_error_response('Not Found', 'Requested Data Not Found', 404)

def not_allowed_handler(err):
    return make_error_response('Not Allowed', 'Method Not Allowed', 405)

def service_error_handler(err):
    return make_error_response('Internal Service Error', 'Unhandled Exception Occurred', 500)


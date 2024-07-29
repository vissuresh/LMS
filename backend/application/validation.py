from flask import jsonify, request
from functools import wraps
from application import db, jwt, models
from flask_jwt_extended import jwt_required, get_jwt, unset_jwt_cookies
from flask_jwt_extended.exceptions import CSRFError

from application import app
import traceback


@app.errorhandler(CSRFError)
def handle_csrf_error(err):
    print("CSRF error")
    print(err)

    traceback.print_exc()
    
    response = jsonify({
        "success":False,
        "message": "CSRF token missing or incorrect",
        "error_type": "csrf",
        "details": str(err)
    })
    response.status_code = 401
    return response


# Check Librarian decorator
def check_librarian(route):

    @jwt_required()
    @wraps(route)
    def wrapper_func(*args, **kwargs):
        claims = get_jwt()
        if claims.get("is_librarian") is False:

            return jsonify({"message":"Forbidden access"}), 403
        
        return route(*args, **kwargs)
    
    return wrapper_func



# Required parameters decorator
def require_keys(*keys):

    def decorator(route):

        @wraps(route)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not all(key in data for key in keys):
                return jsonify({
                    "success" : False,
                    "message" : f"Missing required keys: {', '.join(keys)}"
                }), 400
            return route(*args, **kwargs)
        return decorated_function
    
    return decorator



# Load user
@jwt.user_lookup_loader
def user_lookup_callback(__jwt_headers, jwt_data):
    identity = jwt_data['sub']

    return models.User.get_user_by_email(email = identity)




#additional claims

@jwt.additional_claims_loader
def make_additional_claims(identity):
    user = models.User.get_librarian_by_email(identity)
    if user:
        return {"is_librarian":True}
    return {"is_librarian":False}





### JWT error handlers

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    resp = jsonify({
        "message" : "Token has expired.",
        "error" : "token_expired"
    })
    unset_jwt_cookies(resp)
    return resp, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    resp = jsonify({
        "message" : "Signature verification failed.",
        "error" : "invalid_token"
    })
    unset_jwt_cookies(resp)
    return resp, 401


@jwt.unauthorized_loader
def missing_token_callback(error):

    return jsonify({
        "message" : "Token missing in request",
        "error" : "authorization_header"
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    resp = jsonify({
        "message" : "Token has been revoked",
        "error" : "revoked_token"
    })
    unset_jwt_cookies(resp)
    return resp, 401

### End JWT Error Handlers



# Check if token blocklisted handler

@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):

    print("------ CHECKING BLOCKLIST TOKENS ------")
    
    jti = jwt_data['jti']
    token = db.session.execute(db.select(models.TokenBlocklist).filter_by(jti = jti)).scalar()
    
    return token is not None
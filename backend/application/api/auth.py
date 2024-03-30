from flask import Blueprint, jsonify, request, make_response
from application.validation import require_keys
from application import db
from application.models import User, TokenBlocklist
from sqlalchemy.exc import SQLAlchemyError
import time
from flask_jwt_extended import (create_access_token,
                                create_refresh_token, decode_token,
                                jwt_required,
                                get_jwt, unset_jwt_cookies,
                                current_user,
                                get_jwt_identity)

auth_bp = Blueprint('auth', __name__)


# where is current_user maintained? Any Session table?


@auth_bp.post('/register')
@require_keys('email', 'name', 'password')
def register_user():    

    data = request.get_json()
    
    user = User.get_user_by_email(email = data.get('email'))
    if user is not  None:
        return jsonify({
            "success" : False,
            "message":"Email already exists"
        }), 409
    
    new_user = User(
        email = data.get('email'),
        name = data.get('name')
    )

    new_user.set_password(data.get('password'))
    new_user.save()

    return jsonify({
        "status":"success",
        "message" : "User created"
    }), 201


@auth_bp.post('/login')
@require_keys('email', 'password')
def login_user():
    data = request.get_json()
    user = User.get_user_by_email(email = data.get('email'))
    
    if user and user.check_password(data.get('password')):
        resp = make_response(jsonify({
            "success" : True,
            "message" : "Logged in"
        }), 200)

        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)

        access_exp = decode_token(access_token)['exp']
        refresh_exp = decode_token(refresh_token)['exp']

        resp.set_cookie('access_token_cookie', access_token, samesite=None, secure=False, max_age=access_exp - int(time.time()))
        resp.set_cookie('refresh_token_cookie', refresh_token, samesite=None, secure=False, max_age=refresh_exp - int(time.time()))

        return resp
    
    
    return jsonify({
        "success" : False,
        "message": "Invalid credentials"
    }), 401



@auth_bp.get('/whoami')
@jwt_required()
def whoami():
        
    return jsonify({
        "user_details" : {
            "email":current_user.email,
            "name": current_user.name
        }
    })



@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
   
    new_access_token = create_access_token(identity=identity)
    access_exp = decode_token(new_access_token)['exp']


    resp = make_response(jsonify({
        "success" : True,
        "message" : "Refresh token created"
    }), 200)

    resp.set_cookie('access_token_cookie', new_access_token, samesite=None, secure=False, max_age=access_exp - int(time.time()))

    return resp




@auth_bp.get('/logout')
@jwt_required(refresh = True)
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']

    token_block = TokenBlocklist(jti = jti)
    token_block.save()


    resp = jsonify({"status": "success", "message" : "Refresh token revoked successfully"})
    unset_jwt_cookies(resp)
    return resp, 200






@auth_bp.delete('/')
@jwt_required()
def delete_user():
    for book in current_user.books:
        book.issued -= 1

    db.session.delete(current_user)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "status" : "error",
            "message" : "Transaction failed"
        }), 404
    

    return jsonify({
        "status" : "success",
    }), 200
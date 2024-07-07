from flask import Blueprint, jsonify, request, make_response
from application.validation import require_keys, check_librarian
from application import db, app
from application.models import User, TokenBlocklist
from sqlalchemy.exc import SQLAlchemyError
import time
from flask_jwt_extended import (create_access_token,
                                create_refresh_token, decode_token,
                                jwt_required,
                                get_jwt, unset_jwt_cookies,
                                set_access_cookies,
                                set_refresh_cookies,
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


        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)

        decoded_access_token = decode_token(access_token)
        decoded_refresh_token = decode_token(refresh_token)

        if(decoded_access_token.get('is_librarian') == True):
            resp = make_response(jsonify({
            "success" : True,
            "message" : "Logged in",
            "is_librarian": True
        }), 200)
        else:
            resp = make_response(jsonify({
            "success" : True,
            "message" : "Logged in"
        }), 200)


        access_expiry = decoded_access_token['exp']
        refresh_expiry = decoded_refresh_token['exp']

        set_access_cookies(resp, access_token, max_age= access_expiry - time.time())
        set_refresh_cookies(resp, refresh_token, max_age= refresh_expiry - time.time())

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



@auth_bp.get('/isLibrarian')
@check_librarian
def is_librarian():
    return "OK", 200



@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
   
    new_access_token = create_access_token(identity=identity)
    decoded_access_token = decode_token(new_access_token)
    access_expiry = decoded_access_token['exp']


    if(decoded_access_token.get('is_librarian') == True):
        resp = make_response(jsonify({
        "success" : True,
        "message" : "New access token created",
        "is_librarian": True
    }), 200)
    else:
        resp = make_response(jsonify({
        "success" : True,
        "message" : "New access token created"
    }), 200)

    set_access_cookies(resp, new_access_token, max_age= access_expiry - time.time())
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
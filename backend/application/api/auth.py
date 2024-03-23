from flask import Blueprint, jsonify, request
from application import db
from application.models import User, TokenBlocklist
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt,
                                current_user,
                                get_jwt_identity)

auth_bp = Blueprint('auth', __name__)


# where is current_user maintained? Any Session table?


@auth_bp.post('/register')
def register_user():

    data = request.get_json()
    
    user = User.get_user_by_email(email = data.get('email'))
    if user is not  None:
        return jsonify({'error':"Email already exists"}), 409
    
    new_user = User(
        email = data.get('email'),
        name = data.get('name')
    )

    new_user.set_password(data.get('password'))
    new_user.save()

    return jsonify({"message" : "User created"}), 201


@auth_bp.post('/login')
def login_user():
    data = request.get_json()

    user = User.get_user_by_email(email = data.get('email'))
    
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)

        return jsonify(
            {
                "message" : "Logged in",
                "tokens" : {
                    "access" : access_token,
                    "refresh" : refresh_token
                }
            }
        ), 200
    
    
    return jsonify({'error': 'Invalid credentials'}), 401



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

    return jsonify({"access_t, cascade = 'all, delete'oken" : new_access_token}), 200




@auth_bp.get('/logout')
@jwt_required(refresh = True)
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']

    token_block = TokenBlocklist(jti = jti)
    token_block.save()


    return jsonify({"status": "success", "message" : "Refresh token revoked successfully"}), 200






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
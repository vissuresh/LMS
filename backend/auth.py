from flask import Blueprint, jsonify, request
from models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt

auth_bp = Blueprint('auth', __name__)

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
    claims = get_jwt()
    return jsonify({
        "claims" : claims
    })
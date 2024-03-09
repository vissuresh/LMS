from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from auth import auth_bp
from routes.users import user_bp
from routes.books import book_bp
from routes.sections import section_bp

from models import User, TokenBlocklist


app = Flask(__name__)

# Load config
app.config.from_prefixed_env()


# Load and initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


# Check Librarian decorator
def check_librarian(route):

    @jwt_required()
    def wrapper_func(*args, **kwargs):
        claims = get_jwt()
        if claims.get("is_librarian") is False:

            return jsonify({"message":"Unauthorized access"}), 401
        
        return route(*args, **kwargs)
    
    wrapper_func.__name__ = route.__name__
    
    return wrapper_func


# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(book_bp, url_prefix='/books')
app.register_blueprint(section_bp, url_prefix='/sections')



# Load user
@jwt.user_lookup_loader
def user_lookup_callback(__jwt_headers, jwt_data):
    identity = jwt_data['sub']

    return User.get_user_by_email(email = identity)




#additional claims

@jwt.additional_claims_loader
def make_additional_claims(identity):
    
    if identity == "ksjune13@gmail.com":
        return {"is_librarian":True}
    
    return {"is_librarian":False}





### JWT error handlers

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({
        "message" : "Token has expired.",
        "error" : "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "message" : "Signature verification failed.",
        "error" : "invalid_token"
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "message" : "Token missing in request",
        "error" : "authorization_header"
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return jsonify({
        "message" : "Token has been revoked",
        "error" : "revoked_token"
    }), 401

### End JWT Error Handlers



# Check if token blocklisted handler

@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):

    print("------ CHECKING BLOCKLIST TOKENS ------")
    
    jti = jwt_data['jti']
    token = db.session.execute(db.select(TokenBlocklist).filter_by(jti = jti)).scalar()
    
    return token is not None
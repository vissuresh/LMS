from flask import Flask, jsonify
from extensions import db, jwt, migrate
from auth import auth_bp
from users import user_bp
from models import User

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_prefixed_env()

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app=app, db=db)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')



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
    
    ### End JWT Error Handlers



    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(error):
        pass


    return app
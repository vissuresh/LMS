from flask_jwt_extended import get_jwt, jwt_required
from flask import jsonify

def check_librarian(route):


    @jwt_required()
    def wrapper_func(*args, **kwargs):
        claims = get_jwt()
        if claims.get("is_librarian") is False:

            return jsonify({"message":"Unauthorized access"}), 401
        
        return route(*args, **kwargs)
    
    wrapper_func.__name__ = route.__name__
    
    return wrapper_func
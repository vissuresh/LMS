from flask import Blueprint, request, jsonify
from application import db
from application.models import User
from application.schemas import UserSchema
from application.validation import check_librarian
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy.exc import SQLAlchemyError

user_bp = Blueprint(
    'users',
    __name__
)


@user_bp.get('/all')
@check_librarian
def get_all_users():
    
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)

    try:
        users = User.query.paginate(
            page = page,
            per_page = per_page
        )
    except:
        return jsonify({
            "error": "page or per-page out of bounds"
        }), 400

    result = UserSchema().dump(users, many=True)

    return jsonify({
        "users" : result,

        "pagination": {
            "page": users.page,
            "per_page": users.per_page,
            "total": users.total,
            "pages": users.pages
        }
    }), 200




@user_bp.delete('/')
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
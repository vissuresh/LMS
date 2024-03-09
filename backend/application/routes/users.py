from flask import Blueprint, request, jsonify
from models import User
from schemas import UserSchema
from application import check_librarian

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
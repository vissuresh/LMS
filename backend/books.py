from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import Book
from schemas import BookSchema
from decorators import check_librarian

book_bp = Blueprint(
    'books',
    __name__
)


@book_bp.get('/all')
@jwt_required()
def get_all_books():    
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    try:
        books = Book.query.paginate(
            page = page,
            per_page = per_page
        )
    except:
        return jsonify({
            "error": "page or per-page out of bounds"
        }), 400

    result = BookSchema().dump(books, many=True)    

    return jsonify({
        "books" : result,

        "pagination": {
            "page": books.page,
            "per_page": books.per_page,
            "total": books.total,
            "pages": books.pages
        }
    }), 200


@book_bp.get('/<int:book_id>')
@jwt_required()
def get_book(book_id):
    book = Book.query.get_or_404(book_id)

    return jsonify(BookSchema().dump(book))



@book_bp.post('/')
@check_librarian
def create_book():
    new_book = BookSchema().load(request.json)
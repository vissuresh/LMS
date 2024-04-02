from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from application.models import Book
from application.schemas import BookSchema
from application.validation import check_librarian
from application import db

book_bp = Blueprint(
    'books',
    __name__
)


@book_bp.get('/all')
@jwt_required()
def get_all_books():
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=12, type=int)

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

    return jsonify(BookSchema().dump(book)), 200


@book_bp.get('/user')
@jwt_required()
def get_user_books():
    return jsonify({
        "success" : True,
        "books": BookSchema(exclude=('copies','issued','path',)).dump(current_user.books, many=True)
    }), 200




@book_bp.post('/')
@check_librarian
def create_book():
    new_book = BookSchema().load(request.json, session=db.session)
    new_book.save()
    return jsonify({"message": "success"}), 201



@book_bp.patch('/<int:book_id>')
@check_librarian
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    new_copies = request.json.get('copies')
    if new_copies and new_copies < book.issued:
        return jsonify({
            "status" : "error",
            "message" : "\'copies\' is less than \'issued\'"
        }), 400
    
    BookSchema().load(request.json, instance=book, session=db.session, partial=True)
    book.save()
    
    return jsonify({"message":"success"}), 200



@book_bp.delete('/<int:book_id>')
@check_librarian
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    book.delete()

    return jsonify({"message":"success"}), 200

from flask import Blueprint, jsonify
from application.models import Book
from application.schemas import BookSchema

graphs_bp = Blueprint(
    'graphs',
    __name__
)


@graphs_bp.get('/books/rating')
def get_top_rated_books():
    top_books = Book.query.order_by(Book.rating.desc()).limit(10).all()
    return jsonify(BookSchema(only=("id", "name", "rating")).dump(top_books, many=True)), 200
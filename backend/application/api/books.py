from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, current_user
from application.models import Book
from application.schemas import BookSchema, FeedbackSchema
from application.validation import check_librarian
from application import db
from werkzeug.utils import secure_filename
import os
import json

book_bp = Blueprint(
    'books',
    __name__
)


@book_bp.get('/all')
@jwt_required()
def get_all_books():
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    search_by = request.args.get('search_by', 'book_name')
    search_query = request.args.get('query')
    sections = request.args.get('sections', '').split(',') if request.args.get('sections') else []
    authors = request.args.get('authors', '').split(',') if request.args.get('authors') else []
    rating = int(request.args.get('rating', 0))

    book_query = Book.query

    if search_query not in [None, '']:
        if search_by == 'book_name':
            book_query = book_query.filter(Book.name.ilike(f"%{search_query}%"))
        elif search_by == 'book_id':
            book_query = book_query.filter(Book.id == search_query)

    if sections:
        book_query = book_query.filter(Book.section_id.in_(sections))

    if authors:
        book_query = book_query.filter(Book.author.in_(authors))

    if rating:
        book_query = book_query.filter(Book.rating >= rating)

    book_query = book_query.order_by(Book.date_created.desc())

    try:
        books = book_query.paginate(
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
        "books": BookSchema(exclude=('copies','issued','filename',)).dump(current_user.books, many=True)
    }), 200




@book_bp.post('/')
@check_librarian
def create_book():
    books_dir = current_app.config['BOOKS_DIR']
    data = json.loads(request.form.get('data'))

    data.pop('book_file', None)
    data.pop('issued', None)
    data.pop('rating', None)
    data.pop('id', None)
    data.pop('filename', None)

    new_book = BookSchema().load(data, session=db.session, partial=True)
    db.session.add(new_book)
    db.session.flush()
    db.session.refresh(new_book)

    file = request.files.get('file')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
    

        if file.filename != '':
            file_extension = filename.split('.')[-1].lower()
            if file_extension not in ['pdf', 'epub']:
                return jsonify({
                    "message": "Invalid book file format. Only PDF and EPUB files are allowed"
                }), 400 
            
            new_book.filename = f'{new_book.id}.{file_extension}'

    
    file.save(os.path.join(books_dir, new_book.filename))
    try:
        new_book.save()
    except:
        db.session.rollback()
        os.remove(os.path.join(books_dir, new_book.filename))

        return jsonify({"message": "An error occurred"}), 400
    return jsonify({"message": "success"}), 201



@book_bp.patch('/<int:book_id>')
@check_librarian
def update_book(book_id):
    books_dir = current_app.config['BOOKS_DIR']
    book = Book.query.get_or_404(book_id)

    data = json.loads(request.form.get('data'))
    
    new_copies = data.get('copies')
    if (new_copies is not None) and (new_copies < book.issued):
        return jsonify({
            "message" : "\'copies\' is less than \'issued\'"
        }), 400
    

    data.pop('book_file', None)
    data.pop('issued', None)
    data.pop('rating', None)
    data.pop('id', None)
    data.pop('filename', None)
    
    file = request.files.get('file')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
    

        if file.filename != '':
            file_extension = filename.split('.')[-1].lower()
            if file_extension not in ['pdf', 'epub']:
                return jsonify({
                    "message": "Invalid book file format. Only PDF and EPUB files are allowed"
                }), 400 
            book.filename = f'{book.id}.{file_extension}'


    BookSchema().load(data, instance=book, session=db.session, partial=True)
    
    try:
        book.save()
    except:
        db.session.rollback()
        return jsonify({"message": "An error occurred"}), 400
    
    if file:
        file.save(os.path.join(books_dir, book.filename))

    return jsonify({"message":"success"}), 200



@book_bp.delete('/<int:book_id>')
@check_librarian
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    try:
        book.delete()
    except:
        db.session.rollback()
        return jsonify({"message": "An error occurred"}), 400

    return jsonify({"message":"success"}), 200




@book_bp.get('/authors/all')
@jwt_required()
def get_all_authors():
    authors = db.session.query(Book.author).distinct().all()

    authors_list = []
    for i in range(len(authors)):
        author_obj = {"id": i, "name": authors[i][0]}
        authors_list.append(author_obj)

    return jsonify({"authors": authors_list}), 200




@book_bp.get('/<int:book_id>/comments')
@jwt_required() 
def get_book_feedback(book_id):
    book = Book.query.get_or_404(book_id)

    return jsonify(
        FeedbackSchema().dump(book.feedback, many=True)
    ), 200


@book_bp.post('/<int:book_id>/comments')
@jwt_required()
def submit_feedback(book_id):
    book = Book.query.get_or_404(book_id)
    feedback = FeedbackSchema().load(request.json, session=db.session)
    feedback.book = book
    feedback.user = current_user
    feedback.save()

    update_book_rating(book)

    return jsonify({"message":"success"}), 201



def calculate_average_rating(feedback):
    return round(sum([f.rating for f in feedback]) / len(feedback), 2) if feedback else None


def update_book_rating(book):
    book.rating = calculate_average_rating(book.feedback)
    db.session.commit()
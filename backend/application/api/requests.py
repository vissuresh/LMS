from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from application.models import Book, BookRequest, BookIssue, User
from application.schemas import IssueSchema, RequestSchema, BookSchema
from application.validation import check_librarian
from application import db

from sqlalchemy.exc import SQLAlchemyError

request_bp = Blueprint(
    'requests',
    __name__
)


@request_bp.get('/all')
@check_librarian
def get_all_requests():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    search_query = request.args.get('query')
    books = request.args.get('books', '').split(',') if request.args.get('books') else []
    userEmail = request.args.get('userEmail', '')

    request_query = BookRequest.query

    if search_query not in [None, '']:
        request_query = request_query.filter(BookRequest.id == search_query)

    if books:
        request_query = request_query.filter(BookRequest.book_id.in_(books))

    if userEmail:
        user = User.get_user_by_email(userEmail)
        if user is None:
            return jsonify({
                "message": "User email not found!"
            }), 404
        request_query = request_query.filter(BookRequest.user_id == user.id)

    request_query = request_query.order_by(BookRequest.requested_at.desc())

    try:
        bookRequests = request_query.paginate(
            page = page,
            per_page = per_page
        )
    except:
        return jsonify({
            "error": "page or per-page out of bounds"
        }), 400

    result = RequestSchema().dump(bookRequests, many=True)    

    return jsonify({    
        "requests" : result,

        "pagination": {
            "page": bookRequests.page,
            "per_page": bookRequests.per_page,
            "total": bookRequests.total,
            "pages": bookRequests.pages
        }
    }), 200




@request_bp.get('/user')
@jwt_required()
def get_user_requests():
    return jsonify([ {"book" : BookSchema().dump(request.book), "request_id": request.id} for request in current_user.requests ]), 200



@request_bp.post('/grant/<int:request_id>')
@check_librarian
def grant_book(request_id):
    book_request = BookRequest.query.get_or_404(request_id)
    book = Book.query.get_or_404(book_request.book_id)

    if book.copies == book.issued:
        return jsonify({
            "status" : "error",
            "message" : "Book out of stock"
        }), 400


    data = {"user_id" : book_request.user_id, "book_id" : book_request.book_id}

    book_issue = IssueSchema().load(data, session = db.session)

    db.session.add(book_issue)
    db.session.delete(book_request)

    book.issued += 1

    
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "status" : "error",
            "message" : "Transaction failed"
        }), 404
    
    return jsonify({"status" : "success"}), 200





@request_bp.post('/<int:book_id>')
@jwt_required()
def request_book(book_id):
    
    if len(current_user.books) + len(current_user.requests) == 5:
        return jsonify({
            "message": "User has equalled the limit to borrow."
        }), 409
    
    
    book = Book.query.get_or_404(book_id)
    user_id = current_user.id 

    existing_request = BookRequest.query.filter_by(user_id = user_id, book_id = book_id).first()
    if existing_request:
        return jsonify({
            "message" : "User has already requested this book"
        }), 409
    

    existing_issue = BookIssue.query.filter_by(user_id = current_user.id, book_id = book_id).first()
    if existing_issue:
        return jsonify({
            "status" : "error",
            "message" : "Book already issued to user"
        }), 409

    
    book_request = RequestSchema().load({'user_id':user_id, 'book_id': book_id}, session=db.session)


    response, status_code = book_request.save()
    return response, status_code





@request_bp.delete('/decline/<int:request_id>')
@check_librarian
def admin_delete_request(request_id):
    book_request = BookRequest.query.get_or_404(request_id)

    response, status_code = book_request.delete()
    return response, status_code




@request_bp.delete('/<int:request_id>')
@jwt_required()
def delete_request(request_id):
    book_request = BookRequest.query.get_or_404(request_id)

    if not(book_request.user_id == current_user.id):
        return jsonify({
            "status" : "error",
            "message" : "Unauthorized action"
        }), 403
    
    response, status_code = book_request.delete()
    return response, status_code
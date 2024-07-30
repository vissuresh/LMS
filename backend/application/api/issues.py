from flask import Blueprint, request, jsonify, send_file, url_for, current_app
from flask_jwt_extended import jwt_required, current_user
from application.models import Book, BookIssue, User
from application.schemas import IssueSchema
from application.validation import check_librarian
from application import db, app, serializer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
import os



issue_bp = Blueprint(
    'issues',
    __name__
)


@issue_bp.get('/all')
@check_librarian
def get_all_issues():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    search_query = request.args.get('query')
    books = request.args.get('books', '').split(',') if request.args.get('books') else []
    userEmail = request.args.get('userEmail', '')

    issue_query = BookIssue.query

    if search_query not in [None, '']:
        issue_query = issue_query.filter(BookIssue.id == search_query)

    if books:
        issue_query = issue_query.filter(BookIssue.book_id.in_(books))

    if userEmail:
        user = User.get_user_by_email(userEmail)
        if user is None:
            return jsonify({
                "message": "User email not found!"
            }), 404
        issue_query = issue_query.filter(BookIssue.user_id == user.id)

    issue_query = issue_query.filter(BookIssue.expiry > datetime.now())
    issue_query = issue_query.order_by(BookIssue.issued_at.desc())

    try:
        bookIssues = issue_query.paginate(
            page = page,
            per_page = per_page
        )
    except:
        return jsonify({
            "error": "page or per-page out of bounds"
        }), 400

    result = IssueSchema(exclude=['user_id']).dump(bookIssues, many=True)

    return jsonify({    
        "issues" : result,

        "pagination": {
            "page": bookIssues.page,
            "per_page": bookIssues.per_page,
            "total": bookIssues.total,
            "pages": bookIssues.pages
        }
    }), 200


@issue_bp.delete('/revoke/<int:issue_id>')
@check_librarian
def revoke_book(issue_id):
    issue = BookIssue.query.get_or_404(issue_id)
    book = Book.query.get(issue.book_id)
    
    book.issued -=1
    issue.expiry = datetime.now()

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "status" : "error",
            "message" : "Transaction failed"
        }), 404

    
    return jsonify({
        "status" : "success"
    }), 200




@issue_bp.delete('/return/<int:book_id>')
@jwt_required()
def return_book(book_id):
    issue = BookIssue.query.filter(and_(BookIssue.book_id == book_id, BookIssue.user_id == current_user.id)).first()

    if issue is None:
        return jsonify({"message" : "No such issue found"}), 404
    
    book = Book.query.get(book_id)

    book.issued -=1
    issue.expiry = datetime.now()

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "message" : "Transaction failed"
        }), 404

    
    return jsonify({
        "message" : "success"
    }), 200


@issue_bp.get('/read-book/<int:book_id>')
@jwt_required()
def read_book(book_id):
    issue = BookIssue.query.filter(and_(BookIssue.book_id == book_id, BookIssue.user_id == current_user.id)).first()
    if issue is None:
        return jsonify({"message" : "No such issue found"}), 404
    if issue.expiry < datetime.now():
        return jsonify({"message" : "Issue expired"}), 400

    book = Book.query.get_or_404(issue.book_id)
    books_dir = current_app.config['BOOKS_DIR']

    pdf_path = os.path.join(books_dir, book.filename)
    response = send_file(pdf_path, mimetype='application/pdf')
    response.headers['Content-Disposition'] = response.headers['Content-Disposition'] = 'inline; filename="{}"'.format(book.name.lower().replace(' ', '_'))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response, 200
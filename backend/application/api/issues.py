from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from application.models import Book, BookIssue
from application.schemas import IssueSchema, RequestSchema
from application.validation import check_librarian
from application import db

from sqlalchemy.exc import SQLAlchemyError

issue_bp = Blueprint(
    'issues',
    __name__
)



@issue_bp.delete('/revoke/<int:issue_id>')
@check_librarian
def revoke_book(issue_id):
    issue = BookIssue.query.get_or_404(issue_id)
    book = Book.query.get(issue.book_id)
    
    book.issued -=1
    db.session.delete(issue)

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




@issue_bp.delete('/return/<int:issue_id>')
@jwt_required()
def return_book(issue_id):
    issue = BookIssue.query.get_or_404(issue_id)
    
    if current_user.id != issue.user_id:
        return jsonify({
            "status" : "error",
            "message" : "Unauthorized action"
        }), 403
    
    book = Book.query.get(issue.book_id)

    
    book.issued -=1
    db.session.delete(issue)

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
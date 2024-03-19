from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from application.models import BookIssue, User, Book
from application.schemas import IssueSchema
from application.validation import check_librarian
from application import db

from sqlalchemy.exc import IntegrityError

issue_bp = Blueprint(
    'issues',
    __name__
)


@issue_bp.get('/all')
# @check_librarian
def get_all_issues():
    issues = BookIssue.query.all()
    issue_data = IssueSchema().dump(issues, many=True)

    return jsonify({
        "issues" : issue_data
    }), 200





@issue_bp.post('/')
# @check_librarian
def issue_book():
    data = request.json
    email = data.get('email')
    if email is None:
        return jsonify({"error" : "Invalid data", "Message" : "Missing email"}), 400
    
    user = User.get_user_by_email(email)
    if user is None:
        return jsonify({"error" : "Invalid data", "Message": "User not found"}), 404
    
    data.pop('email')
    data['user_id'] = user.id

    issue = IssueSchema().load(data, session=db.session)
    
    if len(user.issues) == 5:
        return jsonify({
            "error": "Forbidden",
            "message": "User has equalled the limit to borrow."
        })
    
    book = Book.query.get_or_404(data.get('book_id'))
    book.issued += 1
    db.session.add(issue)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error" : "Integrity Error",
            "message" : "Transaction failed"
        }), 402


    return jsonify({
        "message" : "success"
    }), 201
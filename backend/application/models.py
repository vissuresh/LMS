from flask import jsonify
from application import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import CheckConstraint
from sqlalchemy.exc import SQLAlchemyError

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(), primary_key = True, default = lambda: str(uuid4()))
    email = db.Column(db.String(), nullable = False, unique = True)
    password_hash = db.Column(db.String(128), nullable = False)
    name = db.Column(db.String(), nullable = False)


    requests = db.relationship('BookRequest', backref = 'user', cascade = 'all, delete')
    books = db.relationship('Book', secondary = 'book_issue', backref='users')

    def __repr__(self):
        return f"<User {self.email}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email = email).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Librarian(db.Model):
    id = db.Column(db.Integer, default = 1, primary_key = True)
    user_id = db.Column(db.String(), db.ForeignKey('user.id'))

    user = db.relationship('User')

    @classmethod
    def get_all_librarians(cls):
        librarian_objects = cls.query.all()
        return [librarian.user.email for librarian in librarian_objects]
    

    @classmethod
    def get_librarian_by_email(cls, email):
        return cls.query.filter_by(user_id = User.get_user_by_email(email).id).first()


    def revoke_access(self, book_issue_id):
        book_issue = db.get_or_404(BookIssue, book_issue_id)
        book_issue.delete()



class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(), nullable = False)
    created_at = db.Column(db.DateTime(), default = datetime.utcnow)

    def __repr__(self):
        return f"<Token {self.jti}"
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Section(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False, unique = True)
    date_created = db.Column(db.Date, default = datetime.today, nullable = False)
    desc = db.Column(db.String(128))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(64), nullable = False)
    author = db.Column(db.String(64), nullable = False)
    desc = db.Column(db.String(128))
    date_created = db.Column(db.Date, default = datetime.today)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    picture = db.Column(db.LargeBinary)

    copies = db.Column(db.Integer, nullable = False)
    issued = db.Column(db.Integer, nullable = False, default = 0)
    filename = db.Column(db.String(128))

    rating = db.Column(db.Float, default = 0.0, nullable=False)

    section = db.relationship('Section', backref='books')
    feedback = db.relationship('Feedback', backref='book', cascade = 'all, delete')

    __table_args__ = (
        CheckConstraint('issued <= copies', name='check_book_available_constraint'),
    )


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()




class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(), db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    comment = db.Column(db.String(128), nullable = False)
    rating = db.Column(db.Integer, nullable = False)

    user = db.relationship('User')
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()




class BookIssue(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(), db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    issued_at = db.Column(db.DateTime(), nullable = False, default = datetime.utcnow)
    expiry = db.Column(db.DateTime(), nullable = False,default=lambda: datetime.utcnow() + timedelta(days=7))


    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"status": "error", "message" : "Transaction failed"}), 404
        
        return jsonify({"status" : "success"}), 201

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"status": "error", "message" : "Transaction failed"}), 404
        
        return jsonify({"status" : "success"}), 201




class BookRequest(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.String(), db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    requested_at = db.Column(db.DateTime(), nullable = False, default = datetime.utcnow)

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"status": "error", "message" : "Transaction failed"}), 404
        
        return jsonify({"status" : "success", "request_id" : self.id}), 201

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"status": "error", "message" : "Transaction failed"}), 404
        
        return jsonify({"status" : "success"}), 201

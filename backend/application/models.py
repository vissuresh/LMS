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
    librarian = db.Column(db.Boolean, default = False)


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

    @classmethod
    def get_all_librarian_emails(cls):
        return [librarian.email for librarian in cls.query.filter_by(librarian = True).all()]

    @classmethod
    def get_librarian_by_email(cls, email):
        return cls.query.filter_by(email = email, librarian = True).first()  
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(), nullable = False)
    created_at = db.Column(db.DateTime(), default = datetime.now)

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
    rating = db.Column(db.Float, nullable = False)

    date_created = db.Column(db.Date, default = datetime.today)

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

    issued_at = db.Column(db.DateTime(), nullable = False, default = datetime.now)
    expiry = db.Column(db.DateTime(), nullable = False,default=lambda: datetime.now() + timedelta(days=7))


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

    requested_at = db.Column(db.DateTime(), nullable = False, default = datetime.now)

    book = db.relationship('Book', backref='requests')

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"message" : "An error occurred."}), 400
        
        return jsonify({"message" : "Request created for book.", "request_id" : self.id}), 201

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"message" : "Transaction failed"}), 400
        
        return jsonify({"message" : "success"}), 201

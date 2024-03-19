from application import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import CheckConstraint

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(), primary_key = True, default = lambda: str(uuid4()))
    email = db.Column(db.String(), nullable = False, unique = True)
    password_hash = db.Column(db.String(128), nullable = False)
    name = db.Column(db.String(), nullable = False)

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
    name = db.Column(db.String(64), nullable = False)
    date_created = db.Column(db.Date, default = datetime.today, nullable = False)
    desc = db.Column(db.String(128), nullable = False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)
    author = db.Column(db.String(64), nullable = False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))

    copies = db.Column(db.Integer, nullable = False)
    issued = db.Column(db.Integer, nullable = False, default = 0)
    path = db.Column(db.String(128), nullable = False)

    section = db.relationship('Section', backref='books')

    __table_args__ = (
        CheckConstraint('issued <= copies', name='check_book_available_constraint'),
    )


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
    expiry = db.Column(db.DateTime(), nullable = False)

    user = db.relationship('User', backref='issues')
    book = db.relationship('Book', backref='issues')


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
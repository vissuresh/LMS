from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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
    user_id = db.Column(db.String(), db.ForeignKey('user.id'),  primary_key = True)



class TokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    jti = db.Column(db.String(), nullable = False)
    created_at = db.Column(db.DateTime(), default = datetime.utcnow)

    def __repr__(self):
        return f"<Token {self.jti}"
    

    def save(self):
        db.session.add(self)
        db.session.commit()
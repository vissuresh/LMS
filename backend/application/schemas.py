import base64
from marshmallow import fields
from application import db, ma
from application.models import User, Book, Section, BookIssue, BookRequest, Feedback

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ('id', 'email', 'name')
        
    id = ma.auto_field(dump_only = True)
    email = ma.auto_field(dump_only = True)
    name = ma.auto_field(dump_only = True)




class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section
        load_instance = True

    id = ma.auto_field(dump_only = True)
    date_created = ma.auto_field(dump_only = True)
    # books = ma.Nested('BookSchema', many=True, exclude=('section',))



class Base64FileField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is not None:
            return base64.b64encode(value).decode('utf-8')
        
    def _deserialize(self, value, attr, data, **kwargs):
        if value is not None:
            return base64.b64decode(value)
        

class BookShortSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        fields = ('id', 'name')

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
        
    id = ma.auto_field(dump_only = True)
    section = ma.Nested(SectionSchema(only=('id', 'name')), dump_only = True)
    section_id = ma.auto_field(load_only=True)
    filename = ma.auto_field(load_only = True)
    picture = Base64FileField()


class FeedbackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feedback
        load_instance = True

    id = ma.auto_field(dump_only = True)
    user = ma.Method('get_username', dump_only = True)

    def get_username(self, obj):
        return obj.user.name



class IssueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookIssue
        include_fk = True
        include_relationships = True
        load_instance = True

    
    id = ma.auto_field(dump_only = True)
    issued_at = ma.auto_field(dump_only = True)
    expiry = ma.auto_field(dump_only = True)
    user = ma.Method('get_username', dump_only = True)
    book = ma.Method('get_book', dump_only = True)

    def get_username(self, obj):
        user = User.query.get(obj.user_id)
        return UserSchema(exclude=('id',)).dump(user)

    def get_book(self, obj):
        book = Book.query.get(obj.book_id)
        return BookSchema(exclude=('filename', 'picture')).dump(book)






class RequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookRequest
        include_fk = True
        include_relationships = True
        load_instance = True

    id = ma.auto_field(dump_only=True)
    user = fields.Nested(UserSchema(exclude=('id',)), dump_only=True)
    book = ma.Nested(BookSchema(exclude=('filename','picture')))
    user_id = ma.auto_field(load_only=True)

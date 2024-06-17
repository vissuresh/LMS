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



class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
        
    id = ma.auto_field(dump_only = True)
    section = ma.Nested(SectionSchema(only=('id', 'name')), dump_only = True)



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






class RequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookRequest
        include_fk = True
        include_relationships = True
        load_instance = True

    id = ma.auto_field(dump_only = True)

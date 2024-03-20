from application import db, ma
from application.models import User, Book, Section, BookIssue, BookRequest

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ('id', 'email', 'name')
        
    id = ma.auto_field(dump_only = True)
    email = ma.auto_field(dump_only = True)
    name = ma.auto_field(dump_only = True)


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
        include_fk = True
        
    id = ma.auto_field(dump_only = True)



class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only = True)
    date_created = ma.auto_field(dump_only = True)




class IssueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookIssue
        include_fk = True
        include_relationships = True
        load_instance = True

    
    id = ma.auto_field(dump_only = True)
    issued_at = ma.auto_field(dump_only = True)






class RequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookRequest
        include_fk = True
        include_relationships = True
        load_instance = True

    id = ma.auto_field(dump_only = True)

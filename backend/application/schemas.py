from application import db, ma
from application.models import User, Book, Section

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

    
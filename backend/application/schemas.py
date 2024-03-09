from extensions import db
from application import ma
from models import User, Book, Section

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
        sqla_session = db.session
        include_fk = True

    path = ma.auto_field(required=False)



class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section

    
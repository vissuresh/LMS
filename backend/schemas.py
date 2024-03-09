from extensions import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'name')
        
    id = fields.String()
    email = fields.String()
    name = fields.String()


class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

    section_id = fields.Integer(required=True)
    
    copies = fields.Integer(required=True)
    issued = fields.Integer()
    
    path = fields.URL()



class SectionSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    desc = fields.String()

    date_created = fields.Date()


    
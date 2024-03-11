from application import app

from application.api.auth import auth_bp
from application.api.users import user_bp
from application.api.books import book_bp
from application.api.sections import section_bp



# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(book_bp, url_prefix='/books')
app.register_blueprint(section_bp, url_prefix='/sections')
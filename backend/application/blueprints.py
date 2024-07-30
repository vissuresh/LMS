from application import app

from application.api.auth import auth_bp
from application.api.users import user_bp
from application.api.books import book_bp
from application.api.sections import section_bp
from application.api.requests import request_bp
from application.api.issues import issue_bp
from application.tasks import task_bp
    
from flask_sse import sse


# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(book_bp, url_prefix='/books')
app.register_blueprint(section_bp, url_prefix='/sections')
app.register_blueprint(request_bp, url_prefix='/requests')
app.register_blueprint(issue_bp, url_prefix='/issues')
app.register_blueprint(task_bp, url_prefix='/tasks')
app.register_blueprint(sse, url_prefix='/stream')
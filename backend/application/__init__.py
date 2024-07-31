from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from application.config import Config
from application.celery_utils import celery_init_app
from flask_caching import Cache
import os


app = Flask(__name__)

# Load config
app.config['BOOKS_DIR'] = os.path.join(app.instance_path, 'books')
app.config.from_object(Config)


# Load and initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
celery_app = celery_init_app(app)
CORS(app, supports_credentials=True)
cache = Cache(app)


books_dir = app.config['BOOKS_DIR']
if not os.path.exists(books_dir):
    os.makedirs(books_dir)


from application import validation
from application import blueprints


def initialize_database():
    with app.app_context():
        db.create_all()
        from application.models import User
        
        librarian = app.config['LIBRARIAN']
        librarian_email = librarian["email"]
        librarian_object = User.get_librarian_by_email(librarian_email)

        if librarian_object is None:
            print("===== Creating Librarian Account =======")
            librarian_name = librarian["name"]
            librarian_password = librarian["password"]

            librarian_object = User(name=librarian_name, email=librarian_email, librarian=True)
            librarian_object.set_password(librarian_password)
            librarian_object.save()
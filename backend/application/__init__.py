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
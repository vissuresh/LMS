from flask import Flask, jsonify
from itsdangerous import URLSafeTimedSerializer
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from application.config import Config
from application.celery_utils import celery_init_app
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

# print("Celery Configuration:")
# for key, value in celery_app.conf.items():
#     print(f"{key}: {value}")

CORS(app, supports_credentials=True)


books_dir = app.config['BOOKS_DIR']
if not os.path.exists(books_dir):
    os.makedirs(books_dir)

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])



from application import validation
from application import blueprints      
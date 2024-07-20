from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from application.config import Config
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
CORS(app, supports_credentials=True)


books_dir = app.config['BOOKS_DIR']
if not os.path.exists(books_dir):
    os.makedirs(books_dir)



from application import validation
from application import blueprints      
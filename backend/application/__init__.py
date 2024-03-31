from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from application.config import Config


app = Flask(__name__)

# Load config
app.config.from_object(Config)


# Load and initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
CORS(app, supports_credentials=True)

from application import validation
from application import blueprints      
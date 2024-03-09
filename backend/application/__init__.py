from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


app = Flask(__name__)

# Load config
app.config.from_prefixed_env()


# Load and initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from application import validation
from application import blueprints
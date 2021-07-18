from flask import *
from app.config import Config
from flask_restx import Api
from flask_jwt_extended import *
import os
import warnings

warnings.filterwarnings('ignore')

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          version='1.0',
          title='AlgoCamping API server',
          description='algoCamping api server description')

app = Flask(__name__)
# api = Api(app)
app.secret_key = os.urandom(24)
app.config.from_object(Config)
app.config.update(
    DEBUG=True,
    JWT_SECRET_KEY=Config.JWT_SECRET_KEY,
    JWT_EXPIRATION_DELTA=Config.JWT_EXPIRATION_DELTA,
)

jwt = JWTManager(app)

from app.view import routes, apis

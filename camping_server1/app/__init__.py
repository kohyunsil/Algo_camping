from flask import *
import configparser
from app.config import Config
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

import pymysql
import warnings
warnings.filterwarnings('ignore')

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          version='1.0',
          title='AlgoCamping API server',
          description='algoCamping api server description')

app = Flask(__name__)
# api = Api(app)
app.config.from_object(Config)


from app.view import routes, apis

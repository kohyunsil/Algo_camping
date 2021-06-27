from flask import *
from app.config import Config
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
import pymysql


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
pymysql.install_as_MySQLdb()

from app.view import routes, apis

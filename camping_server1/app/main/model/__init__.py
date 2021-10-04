from app.config import DBConfig
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from ..util import place_dto, modeling_dto
from flask_migrate import Migrate

# SQLAlchemy
migrate = Migrate()
db = SQLAlchemy()
pymysql.install_as_MySQLdb()

client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
Base = declarative_base(client)

# MongoEngine
mongodb = MongoEngine()

# place dto
place_dto = place_dto.PlaceDTO()
modeling_dto = modeling_dto.ModelingDTO()
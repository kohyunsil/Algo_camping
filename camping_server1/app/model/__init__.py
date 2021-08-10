from app.config import Config
import pymysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from ..util import place_dto, modeling_dto
from app import app

# SQLAlchemy
db = SQLAlchemy(app)
pymysql.install_as_MySQLdb()

client = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base(client)

# place dto
place_dto = place_dto.PlaceDTO()
modeling_dto = modeling_dto.ModelingDTO()
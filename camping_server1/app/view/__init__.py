from app.config import Config
import pymysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import app

# SQLAlchemy
db = SQLAlchemy(app)
pymysql.install_as_MySQLdb()

client = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base(client)

Session = sessionmaker(bind=client)
session_ = Session()


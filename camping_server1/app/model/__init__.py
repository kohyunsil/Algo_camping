from app import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine, autoflush=False)()
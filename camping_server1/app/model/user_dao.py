from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from ..model import db


@dataclass
class UserDAO(db.Model):
    __tablename__ = 'user'

    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(255), primary_key=False)
    name = Column(db.String(50), primary_key=False)
    password = Column(db.String(255), primary_key=False)
    created_date = Column(db.String(255), primary_key=False)
    modified_date = Column(db.String(255), primary_key=False)

    def __init__(self, email, name, password, created_date, modified_date):
        self.email = email
        self.name = name
        self.password = password
        self.created_date = created_date
        self.modified_date = modified_date

db.create_all()

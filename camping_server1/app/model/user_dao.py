from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from ..model import db

@dataclass
class UserDAO(db.Model):

    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id: int
    user_name: str
    email: str

    id = Column(db.Integer, primary_key=True)
    user_name = Column(db.String(50), primary_key=False)
    email = Column(db.String(255), primary_key=False)


    def __init__(self, user_name, email):
        self.user_name = user_name
        self.email = email

db.create_all()
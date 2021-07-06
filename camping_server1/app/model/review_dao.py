from dataclasses import dataclass
from sqlalchemy import Column
from ..model import db


@dataclass
class ReviewDAO(db.Model):

    __tablename__ = 'review'
    __table_args__ = {'extend_existing': True, 'mysql_collate': 'utf8_general_ci'}
    id: int
    place_id: int
    star: float

    id = Column(db.Integer, primary_key=True)
    place_id = Column(db.Integer, primary_key=False)
    star = Column(db.Float, primary_key=False)

    def __init__(self, place_id, star):
        self.place_id = place_id
        self.star = star

db.create_all()

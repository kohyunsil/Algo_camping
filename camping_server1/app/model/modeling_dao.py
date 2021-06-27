from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from ..model import db

@dataclass
class ModelingDAO(db.Model):

    __tablename__ = 'modeling'
    __table_args__ = {'extend_existing': True}
    id: int
    place_name: str
    addr: str
    main_cat: str
    sub_cat: str
    weight: int

    id = Column(db.Integer, primary_key=True),
    place_name = Column(db.String(255), primary_key=False),
    addr = Column(db.String(255), primary_key=False),
    main_cat = Column(db.String(255), primary_key=False),
    sub_cat = Column(db.String(255), primary_key=False),
    weight = Column(db.Integer, primary_key=False)

    def __init__(self, place_name, addr, main_cat, sub_cat, weight):
        self.place_name = place_name
        self.addr = addr
        self.main_cat = main_cat
        self.sub_cat = sub_cat
        self.weight = weight

db.create_all()
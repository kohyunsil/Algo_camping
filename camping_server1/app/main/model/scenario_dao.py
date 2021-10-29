from dataclasses import dataclass
from sqlalchemy import Column
from ..model import db


@dataclass()
class ScenarioDAO(db.Model):
    __tablename__ = 'scenario'

    id = Column(db.Integer, primary_key=True)
    scene_no = Column(db.String(255), primary_key=False)
    copy = Column(db.String(255), primary_key=False)
    content_id = Column(db.Integer, primary_key=False)
    place_name = Column(db.String, primary_key=False)

    a100 = Column(db.Integer, primary_key=False)
    a200 = Column(db.Integer, primary_key=False)
    a210 = Column(db.Integer, primary_key=False)
    a300 = Column(db.Integer, primary_key=False)
    a410 = Column(db.Integer, primary_key=False)
    a420 = Column(db.Integer, primary_key=False)
    a500 = Column(db.Integer, primary_key=False)
    a600 = Column(db.Integer, primary_key=False)

    spot1 = Column(db.Integer, primary_key=False)
    spot2 = Column(db.Integer, primary_key=False)
    first_image = Column(db.String(255), primary_key=False)

    def __init__(self, id, scene_no, copy, content_id, place_name,
                 a100, a200, a210, a300, a410, a420, a500, a600,
                 spot1, spot2, first_image):
        self.id = id
        self.scene_no = scene_no
        self.copy = copy
        self.content_id = content_id
        self.place_name = place_name
        self.a100 = a100
        self.a200 = a200
        self.a210 = a210
        self.a300 = a300
        self.a410 = a410
        self.a420 = a420
        self.a500 = a500
        self.a600 = a600
        self.spot1 = spot1
        self.spot2 = spot2
        self.first_image = first_image
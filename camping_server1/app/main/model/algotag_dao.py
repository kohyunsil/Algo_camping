from dataclasses import dataclass
from sqlalchemy import Column
from ..model import db


@dataclass
class AlgoTagDAO(db.Model):
    __tablename__ = 'algotag'
    __table_args__ = {'extend_existing': True, 'mysql_collate': 'utf8_general_ci'}

    id: int
    content_id: int
    tag: str
    point: float

    id = Column(db.Integer, primary_key=True)
    content_id = Column(db.Integer, primary_key=False)
    tag = Column(db.String(50), primary_key=False)
    point = Column(db.Float, primary_key=False)

    def __init__(self, id, content_id, tag, point):
        self.id = id
        self.content_id = content_id
        self.tag = tag
        self.point = point

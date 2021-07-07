from dataclasses import dataclass
from sqlalchemy import Column
from ..model import db


@dataclass
class CongestionDAO(db.Model):
    __tablename__ = 'congestion'
    __table_args__ = {'extend_existing': True, 'mysql_collate': 'utf8_general_ci'}
    id: int
    sigungu_code: int
    base_ymd: str
    congestion: int
    content_id: int

    id = Column(db.Integer, primary_key=True)
    sigungu_code = Column(db.Integer, primary_key=False)
    base_ymd = Column(db.String(50), primary_key=False)
    congestion = Column(db.Integer, primary_key=False)
    content_id = Column(db.Integer, primary_key=False)

    def __init__(self, sigungu_code, base_ymd, congestion, content_id):
        self.sigungu_code = sigungu_code
        self.base_ymd = base_ymd
        self.congestion = congestion
        self.content_id = content_id

db.create_all()
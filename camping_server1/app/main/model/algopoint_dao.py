from dataclasses import dataclass
from sqlalchemy import Column
from ..model import db


@dataclass
class AlgoPointDAO(db.Model):
    __tablename__ = 'algopoint'

    content_id = Column(db.Integer, primary_key=True)
    comfort = Column(db.Float, primary_key=False)
    together = Column(db.Float, primary_key=False)
    fun = Column(db.Float, primary_key=False)
    healing = Column(db.Float, primary_key=False)
    clean = Column(db.Float, primary_key=False)
    algostar = Column(db.Float, primary_key=False)

    def __init__(self, content_id, comfort, together, fun, healing, clean, algostar):
        self.content_id = content_id
        self.comfort = comfort
        self.together = together
        self.fun = fun
        self.healing = healing
        self.clean = clean
        self.algostar = algostar
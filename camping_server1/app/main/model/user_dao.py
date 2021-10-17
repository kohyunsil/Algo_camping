from dataclasses import dataclass
from sqlalchemy import Column
from ..model import db


@dataclass
class UserDAO(db.Model):
    __tablename__ = 'user'

    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(255), primary_key=False)
    name = Column(db.String(50), primary_key=False)
    password = Column(db.String(255), primary_key=False)
    nickname = Column(db.String(255), primary_key=False)
    birth_date = Column(db.Integer, primary_key=False)
    access_token = Column(db.String(255), primary_key=False)
    created_date = Column(db.String(255), primary_key=False)
    modified_date = Column(db.String(255), primary_key=False)

    A100 = Column(db.Integer, primary_key=False)
    A200 = Column(db.Integer, primary_key=False)
    A210 = Column(db.Integer, primary_key=False)
    A300 = Column(db.Integer, primary_key=False)
    A410 = Column(db.Integer, primary_key=False)
    A420 = Column(db.Integer, primary_key=False)
    A500 = Column(db.Integer, primary_key=False)
    A600 = Column(db.Integer, primary_key=False)

    comfort = Column(db.Float, primary_key=False)
    together = Column(db.Float, primary_key=False)
    fun = Column(db.Float, primary_key=False)
    healing = Column(db.Float, primary_key=False)
    clean = Column(db.Float, primary_key=False)

    like = Column(db.String(255), primary_key=False)
    member = Column(db.Integer, primary_key=False)


    def __init__(self, email, name, password, nickname, birth_date, access_token, created_date, modified_date,
                 A100, A200, A210, A300, A410, A420, A500, A600,
                 comfort, together, fun, healing, clean, like, member):
        self.email = email
        self.name = name
        self.password = password
        self.nickname = nickname
        self.birth_date = birth_date
        self.access_token = access_token
        self.created_date = created_date
        self.modified_date = modified_date
        self.A100 = A100
        self.A200 = A200
        self.A210 = A210
        self.A300 = A300
        self.A410 = A410
        self.A420 = A420
        self.A500 = A500
        self.A600 = A600
        self.comfort = comfort
        self.together = together
        self.fun = fun
        self.healing = healing
        self.clean = clean
        self.like = like
        self.member = member
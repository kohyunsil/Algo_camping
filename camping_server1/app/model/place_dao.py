from dataclasses import dataclass
from sqlalchemy import Column
from ..model import db


@dataclass
class PlaceDAO(db.Model):

    __tablename__ = 'place'
    __table_args__ = {'extend_existing': True, 'mysql_collate': 'utf8_general_ci'}
    id: int
    place_num: int
    place_name: str
    content_id: int
    sigungu_code: int
    addr: str
    lat: float
    lng: float
    event_start_date: str
    event_end_date: str
    first_image: str
    second_image: str
    detail_image: str
    tel: str
    tag: str
    homepage: str
    line_intro: str
    readcount: int
    industry: str
    oper_date: str
    oper_pd: str
    modified_date: str

    id = Column(db.Integer, primary_key=True)
    place_num = Column(db.Integer, primary_key=False)
    place_name = Column(db.String(50), primary_key=False)
    content_id = Column(db.Integer, primary_key=False)
    sigungu_code = Column(db.Integer, primary_key=False)
    addr = Column(db.String(50), primary_key=False)
    lat = Column(db.Float, primary_key=False)
    lng = Column(db.Float, primary_key=False)
    event_start_date = Column(db.DateTime)
    event_end_date = Column(db.DateTime)
    first_image = Column(db.String, primary_key=False)
    second_image = Column(db.String, primary_key=False)
    detail_image = Column(db.String, primary_key=False)
    tel = Column(db.String, primary_key=False)
    tag = Column(db.String, primary_key=False)
    homepage = Column(db.String, primary_key=False)
    line_intro = Column(db.String, primary_key=False)
    readcount = Column(db.Integer, primary_key=False)
    industry = Column(db.String, primary_key=False)
    oper_date = Column(db.String, primary_key=False)
    oper_pd = Column(db.String, primary_key=False)
    modified_date = Column(db.String, primary_key=False)

    def __init__(self, place_num, place_name, content_id, sigungu_code, addr, lat, lng,
                 event_start_date, event_end_date, first_image,
                 second_image, detail_image, tel, tag, homepage, line_intro,
                 readcount, industry, oper_date, oper_pd, modified_date):
        self.place_num = place_num
        self.place_name = place_name
        self.content_id = content_id
        self.sigungu_code = sigungu_code
        self.addr = addr
        self.lat = lat
        self.lng = lng
        self.event_start_date = event_start_date
        self.event_end_date = event_end_date
        self.first_image = first_image
        self.second_image = second_image
        self.detail_image = detail_image
        self.tel = tel
        self.tag = tag
        self.homepage = homepage
        self.line_intro = line_intro
        self.readcount = readcount
        self.industry = industry
        self.oper_date = oper_date
        self.oper_pd = oper_pd
        self.modified_date = modified_date

db.create_all()
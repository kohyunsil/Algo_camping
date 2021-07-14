from ..model.review_dao import ReviewDAO as model_review
from ..model.congestion_dao import CongestionDAO as model_congestion
from ..model.place_dao import PlaceDAO as model_place
from ..model.user_dao import UserDAO as model_user
from ..service.search import get_score
from sqlalchemy.orm import sessionmaker
from ..model import *
from flask import *
from ..config import Config
import datetime

# 이메일 중복 체크
def check_duplicate(param):
    email = param['email']
    '''
    # select email from user where email = 'param['email']';
    '''
    Session = sessionmaker(bind=client)
    session_ = Session()

    query = session_.query(model_user).filter(model_user.email == email)


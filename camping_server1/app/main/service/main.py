from flask import *
from .user import is_exist_user
import numpy as np
from app.config import Config
from app.main.model.userevent_dao import UserEventDAO as model_userevent
from app.main.model.userevent_dao import Param as model_param
import pymongo

def save_swiper_log(param):
    position = param['id']
    if is_exist_user():
        id = is_exist_user()['id']
        is_signin = 1
    else:
        id = np.random.randint(Config.RANDOM_RANGE, Config.RANDOM_RANGE * 10)
        is_signin = 0

    userevent = model_userevent(isSignin=is_signin, userNo=id, screen='/main', action='click')
    userevent.param = model_param(type='banner', position=position, keyword=None)
    userevent.save()

    return jsonify({'code': 200})
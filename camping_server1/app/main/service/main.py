from flask import *
from .user import is_exist_user
from app.main.service import user
import numpy as np
from app.config import Config
from app.main.model.userevent_dao import UserEventDAO as model_userevent
from app.main.model.userevent_dao import Param as model_param
import pymongo
import datetime
import logging

def user_event_logging(headers, base_url, screen, method, action, type, keyword, param=None):
    position = None
    if param is not None:
        position = param['id']

    if is_exist_user():
        id = is_exist_user()['id']
        is_signin = 1
    else:
        id = np.random.randint(Config.RANDOM_RANGE, Config.RANDOM_RANGE * 10)
        is_signin = 0

    try:
        userevent = model_userevent(headers=headers, isSignin=is_signin, userNo=id, baseUrl=base_url, screen=screen, method=method, action=action)
        userevent.param = model_param(type=type, position=position, keyword=keyword)
        userevent.save()

        logging.info('----[' + str(datetime.datetime.now()) + ' user_event_logging() : 200]----')
        return jsonify({'code': 200})
    except:
        logging.error('----[' + str(datetime.datetime.now()) + ' user_event_logging() : 500]----')
        return jsonify({'code': 500})
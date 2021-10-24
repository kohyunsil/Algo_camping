from flask import *
from .user import is_exist_user
from app.main.service import user
import numpy as np
from app.config import Config
from app.main.model import *
from app.main.model.userevent_dao import UserEventDAO as model_userevent
from app.main.model.userevent_dao import Param as model_param
from app.main.model.scenario_dao import ScenarioDAO as model_scenario
from app.main.model.user_dao import UserDAO as model_user
from sqlalchemy.orm import session
from sqlalchemy.orm import sessionmaker
import pymongo
import datetime
import logging
import random

def user_event_logging(headers, base_url, screen, method, action, type, keyword, param=None, page=None):
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
        userevent.param = model_param(type=type, position=position, keyword=keyword, page=page)
        userevent.save()

        logging.info('----[' + str(datetime.datetime.now()) + ' user_event_logging() : 200]----')
        return jsonify({'code': 200})
    except:
        logging.error('----[' + str(datetime.datetime.now()) + ' user_event_logging() : 500]----')
        return jsonify({'code': 500})

def get_recommend_swiper():
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()

    param = dict()
    copy_list, content_id_list, place_name_list, first_image_list = list(), list(), list(), list()

    try:
        rand_idx = random.randint(0, 5)
        '''
        # SELECT DISTINCTROW copy FROM camping.scenario WHERE spot1=1;
        '''
        copy_obj = session_.query(model_scenario).distinct(model_scenario.copy).filter(
            model_scenario.spot1 == 1
        ).group_by(model_scenario.copy).all()

        copy_obj_list = [obj.copy for obj in copy_obj]
        rand_copy = copy_obj_list[random.randint(0, len(copy_obj_list)-1)]

        '''
        # SELECT * FROM scenario WHERE copy = rand_copy and spot1=1;
        '''
        recommend_query = session_.query(model_scenario).filter(
            and_(model_scenario.copy == rand_copy, model_scenario.spot1 == 1)
        ).all()

        query_res_len = len(recommend_query)
        rand_list = list()
        max_res_len = 5

        for _ in range(max_res_len):
            rand_num = random.randint(0, query_res_len-1)
            if rand_num in rand_list:
                while True:
                    rand_num = random.randint(0, query_res_len-1)
                    if rand_num not in rand_list:
                        rand_list.append(rand_num)
                        break
            else:
                rand_list.append(rand_num)

        # 반환되는 scenario list
        for i, recommend_obj in enumerate(recommend_query):
            if i in rand_list:
                copy_list.append(recommend_obj.copy)
                content_id_list.append(recommend_obj.content_id)
                place_name_list.append(recommend_obj.place_name)
                first_image_list.append(recommend_obj.first_image)

        param['copy'] = copy_list
        param['content_id'] = content_id_list
        param['place_name'] = place_name_list
        param['first_image'] = first_image_list
        param['code'] = 200

        logging.info('----[' + str(datetime.datetime.now()) + ' get_recommend_swiper() : 200]----')
    except:
        logging.error('----[' + str(datetime.datetime.now()) + ' get_recommend_swiper() : 500]----')
    finally:
        session_.close()
    return param

def get_user_recommend_swiper(param):
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()

    try:
        '''
        # SELECT A100, A200, A210, A300, A410, A420, A500, A600 FROM user WHERE access_token = access_token;
        '''
        user_survey_query = session_.query(model_user.A100, model_user.A200, model_user.A210, model_user.A300,
                                           model_user.A410, model_user.A420, model_user.A500, model_user.A600).filter(
            model_user.access_token == param['access_token']).all()

        A100_u, A200_u, A210_u, A300_u, A410_u, A420_u, A500_u, A600_u = 0, 0, 0, 0, 0, 0, 0, 0
        content_id_list, place_name_list, first_image_list, copy_list = list(), list(), list(), list()

        for user_survey_obj in user_survey_query:
            A100_u = int(user_survey_obj.A100)
            A200_u = int(user_survey_obj.A200)
            A210_u = int(user_survey_obj.A210)
            A300_u = int(user_survey_obj.A300)
            A410_u = int(user_survey_obj.A410)
            A420_u = int(user_survey_obj.A420)
            A500_u = int(user_survey_obj.A500)
            A600_u = int(user_survey_obj.A600)

        # 설문결과가 0인 경우 (kakao login)
        # if A100_u == 0 and A200_u == 0 and A210_u == 0 and A300_u == 0 and A410_u == 0 and A420_u == 0 and A500_u == 0 and A600_u == 0:
        #     return get_recommend_swiper()
        # else:
        '''
        # SELECT * FROM scenario WHERE spot1 = 1 and a100 = user a100
        # UNION ALL SELECT * FROM scenario WHERE spot1 = 1 and a200 = user a200
        # UNION ALL SELECT * FROM scenario WHERE spot1= 1 AND a210 = user a210
        # UNION ALL SELECT * FROM scenario WHERE spot1= 1 AND a300 = user a300
        # UNION ALL SELECT * FROM scenario WHERE spot1= 1 AND a410 = user a410
        # UNION ALL SELECT * FROM scenario WHERE spot1= 1 AND a420 = user a420
        # UNION ALL SELECT * FROM scenario WHERE spot1= 1 AND a500 = user a500
        # UNION ALL SELECT * FROM scenario WHERE spot1= 1 AND a600 = user a600;
        '''

        a100_query = session_.query(model_scenario).filter(and_(model_scenario.spot1 == 1, model_scenario.a200 == A100_u))
        a200_query = session_.query(model_scenario).filter(and_(model_scenario.spot1 == 1, model_scenario.a200 == A200_u))
        a210_query = session_.query(model_scenario).filter(and_(model_scenario.spot1 == 1, model_scenario.a210 == A210_u))
        a300_query = session_.query(model_scenario).filter(and_(model_scenario.spot1 == 1, model_scenario.a300 == A300_u))
        a410_query = session_.query(model_scenario).filter(and_(model_scenario.spot1 == 1, model_scenario.a410 == A410_u))
        a420_query = session_.query(model_scenario).filter(and_(model_scenario.spot1 == 1, model_scenario.a420 == A420_u))
        a500_query = session_.query(model_scenario).filter(and_(model_scenario.spot1 == 1, model_scenario.a500 == A500_u))
        a600_query = session_.query(model_scenario).filter(and_(model_scenario.spot1 == 1, model_scenario.a600 == A600_u))

        user_recommend_query = a100_query.union_all(a200_query, a210_query, a300_query, a410_query, a420_query, a500_query, a600_query).all()

        max_res_len = 5
        query_res_len = len(user_recommend_query)
        rand_list = list()

        for _ in range(max_res_len):
            rand_num = random.randint(0, query_res_len-1)
            if rand_num in rand_list:
                while True:
                    rand_num = random.randint(0, query_res_len-1)
                    if rand_num not in rand_list:
                        rand_list.append(rand_num)
                        break
            else:
                rand_list.append(rand_num)

        # 반환되는 유저 scenario list
        for i, recommend_obj in enumerate(user_recommend_query):
            if i in rand_list:
                copy_list.append(recommend_obj.copy)
                content_id_list.append(recommend_obj.content_id)
                place_name_list.append(recommend_obj.place_name)
                first_image_list.append(recommend_obj.first_image)

        param['content_id'] = content_id_list
        param['place_name'] = place_name_list
        param['first_image'] = first_image_list
        param['copy'] = copy_list
        param['code'] = 200

        logging.info('----[' + str(datetime.datetime.now()) + ' get_user_recommend_swiper() : 200]----')
    except:
        logging.error('----[' + str(datetime.datetime.now()) + ' get_user_recommend_swiper() : 500]----')
    finally:
        session_.close()

    return param

def get_swiper_banner():
    mass_scenario = ['s101', 's102', 's105', 's107', 's111', 's112', 's115', 's119']

    DEFAULT_PATH = '/static/imgs/banner_imgs/'
    mass_img_url = [DEFAULT_PATH + 'with_child.jpeg', DEFAULT_PATH + 'ocean.jpeg',
                    DEFAULT_PATH + 'tour.jpeg', DEFAULT_PATH + 'autumn.jpeg',
                    DEFAULT_PATH + 'with_pet.jpeg', DEFAULT_PATH + 'jeju.jpeg',
                    DEFAULT_PATH + 'with_family.jpeg', DEFAULT_PATH + 'with_couple.jpeg']

    mass_img = {scenario: mass_img_url[i] for i, scenario in enumerate(mass_scenario)}

    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()

    param = dict()
    try:
        '''
        # SELECT DISTINCT scene_no, copy FROM scenario WHERE spot2 = 1;
        '''
        banner_query = session_.query(model_scenario.scene_no, model_scenario.copy).distinct(model_scenario.scene_no, model_scenario.copy).filter(
            model_scenario.spot2 == 1
        ).all()

        max_res_len = 3
        rand_range = len(banner_query)
        rand_list = list()

        for _ in range(max_res_len):
            rand_num = random.randint(0, rand_range - 1)
            if rand_num in rand_list:
                while True:
                    rand_num = random.randint(0, rand_range - 1)
                    if rand_num not in rand_list:
                        rand_list.append(rand_num)
                        break
            else:
                rand_list.append(rand_num)

        copy_list, scene_no_list = list(), list()

        # 반환되는 scenario list
        for idx in rand_list:
            copy_list.append(banner_query[idx].copy)
            scene_no_list.append(banner_query[idx].scene_no)

        first_img_list = [mass_img[no] for no in scene_no_list]

        param['copy'] = copy_list
        param['scene_no'] = scene_no_list
        param['first_image'] = first_img_list
        param['code'] = 200

        logging.info('----[' + str(datetime.datetime.now()) + ' get_swiper_banner() : 200]----')
    except:
        logging.error('----[' + str(datetime.datetime.now()) + ' get_swiper_banner() : 500]----')
        param['code'] = 500
    finally:
        session_.close()
    return param
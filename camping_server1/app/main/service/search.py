from app.main.model.place_dao import PlaceDAO as model_place
from app.main.model.search_dao import SearchDAO as model_search
from app.main.model.algopoint_dao import AlgoPointDAO as model_algopoint
from app.main.model.user_dao import UserDAO as model_user
from app.main.model.scenario_dao import ScenarioDAO as model_scenario
from app.main.model import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from flask import *
from operator import itemgetter
from app.config import Config
from ..service.tag_points import TagPoints
import datetime
import pandas as pd
import logging
from app.main.service.user_points import PolarArea
from ..model.connect import Query

# 검색결과 리스트
def get_tag_searchlist(params, res_len, page):
    split_params = []

    for param in params['keywords'].split(';'):
        if param != '':
            split_params.append(param)

    place_keyword, area = ' ', ' '
    category_keyword = []

    # 입력 데이터 태그/캠핑장 구분
    for i, param in enumerate(split_params):
        if i == 0:
            if split_params[0] == '지역':
                continue
            else:
                area = '%{}%'.format(split_params[0].replace(' ', '')).split('%')[1].strip()
                area = ' ' if area == '지역전체' else area
        else:
            search = '%{}%'.format(param.replace(' ', ''))
            row = model_search.query.filter(model_search.tag.like(search)).all()

            if len(row) == 0:
                place_keyword = search
            else:
                if Config.TAGS.get(param.replace(' ', '')) is not None:
                    category_keyword.append(Config.TAGS[param.replace(' ', '')])

    # 태그 컬럼명과 동적 매칭
    tag_query = ''
    if len(category_keyword) == 0:
        tag_query = ' '
    else:
        for tag in category_keyword:
            tag_query += 'or' + tag

            if category_keyword[len(category_keyword) - 1] == tag:
                tag_query += ' = 1'
            else:
                tag_query += ' = 1 or '

    offset = (page * Config.LIMIT_LEN) - Config.LIMIT_LEN
    db = Query()
    try:
        cursor, engine, mydb = db.connect_sql()
        query = f"(select * from place where content_id in(\
                select content_id from search where addr like '%{area}%' or place_name like '%{place_keyword}%' or '%{tag_query}%') and place_num = 0 order by (case \
                when place_name like '%{place_keyword}%' and addr like '%{area}%' then 1\
                when place_name like '%{place_keyword}%' or addr like '%{area}%' then 2\
                when addr like '%{area}%' then 3\
                else 4\
                end) limit {offset}, {Config.LIMIT_LEN});"

        cursor.execute(query)
        result = cursor.fetchall()

        content_id, place_info = [], []
        for res in result:
            res['tag'] = str(res['tag']).split('#')[1:4]
            res['detail_image'] = str(res['detail_image']).split(',')[:5]
            content_id.append(res['content_id'])
            place_info.append(res)
            res['modified_date'] = str(res['modified_date'])
    except:
        params['code'] = 500

    algo_stars, algo_scores = get_score(content_id)
    tags = get_top_tag(content_id, 3)
    match_pct = get_matching_rate(content_id) if get_matching_rate(content_id) else False

    # setter
    place_dto.place = place_info
    modeling_dto.modeling = {'algo_stars': algo_stars, 'tags': tags}

    logging.info('----[' + str(datetime.datetime.now()) + ' get_searchlist() : 200]----')

    # 지역만 검색 시
    params['flag'] = False
    if len(tag_query) == 1 and len(place_keyword) == 1:
        params['flag'] = True

    params['code'] = 200
    params['keywords'] = ', '.join(split_params)
    params['res_num'] = len(result)
    params['place_info'] = place_info
    params['algo_star'] = algo_stars
    params['algo_score'] = algo_scores
    params['tag'] = tags
    if match_pct is not False:
        params['match_pct'] = match_pct

    return params

# row 수
def get_row_nums(params):
    split_params = []

    for param in params['keywords'].split(';'):
        if param != '':
            split_params.append(param)

    place_keyword, area = '', ''
    category_keyword = []

    # 입력 데이터 태그/캠핑장 구분
    for i, param in enumerate(split_params):
        if i == 0:
            if split_params[0] == '지역':
                continue
            else:
                area = '%{}%'.format(split_params[0].replace(' ', ''))
        else:
            search = '%{}%'.format(param.replace(' ', ''))
            row = model_search.query.filter(model_search.tag.like(search)).all()

            if len(row) == 0:
                place_keyword = search
            else:
                if Config.TAGS.get(param.replace(' ', '')) is not None:
                    category_keyword.append(Config.TAGS[param.replace(' ', '')])

    # 태그 컬럼명과 동적 매칭
    tag_query = ''
    for tag in category_keyword:
        tag_query += tag

        if category_keyword[len(category_keyword) - 1] == tag:
            tag_query += ' = 1'
        else:
            tag_query += ' = 1 or '

    '''
    # SELECT count(*) FROM place WHERE place_num = 0 AND content_id IN(
    # SELECT content_id FROM search WHERE addr LIKE '%지역%' OR place_name LIKE '%캠핑장명%' OR (태그1=1 OR 태그2=1)) ORDER BY (CASE 
    # WHEN place_name LIKE '%캠핑장명%' AND  addr LIKE '%전체%' THEN 1
    # WHEN place_name LIKE '%캠핑장명%' OR addr LIKE '%전체%' THEN 2
    # WHEN addr LIKE '%지역%' THEN 3
    # ELSE 4
    # END);
    '''
    Session = sessionmaker(bind=client)
    session_ = Session()
    try:
        if tag_query == '':
            sub_query = session_.query(model_search.content_id).filter(model_search.addr.like(area) |
                                                                       model_search.place_name.like(place_keyword))
        else:
            sub_query = session_.query(model_search.content_id).filter(model_search.addr.like(area) |
                                                                       model_search.place_name.like(place_keyword) |
                                                                       text(tag_query))

        main_query = session_.query(func.count()).filter(
            and_(model_place.place_num == 0, model_place.content_id.in_(sub_query))).order_by(
            case(
                (and_(model_place.place_name.contains(place_keyword), model_place.addr.contains(area)), 1),
                (or_(model_place.place_name.contains(place_keyword), model_place.addr.contains(area)), 2),
                (model_place.addr.contains(area), 3),
                else_=4
            )
        ).all()

    finally:
        session_.close()

    logging.info('----[' + str(datetime.datetime.now()) + ' get_row_nums() : 200]----')

    res_param = dict()
    res_param['code'] = 200
    res_param['row_nums'] = int(main_query[0][0])

    return jsonify(res_param)

# 유저-캠핑장 매칭도
def get_matching_rate(content_id):
    try:
        if session['access_token']:
            match_result = []
            param = dict()
            client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
            Session = sessionmaker(bind=client)
            session_ = Session()
            if type(content_id) == list:
                for id in content_id:
                    try:
                        '''
                        # SELECT * FROM algopoint WHERE content_id = id;
                        '''
                        algopoint_query = session_.query(model_algopoint.comfort, model_algopoint.together,
                                                         model_algopoint.fun, model_algopoint.healing, model_algopoint.clean).filter(model_algopoint.content_id == int(id)).all()
                        '''
                        # SELECT comfort, together, fun, healing, clean FROM user WHERE access_token = session['access_token'] 
                        '''
                        userpoint_query = session_.query(model_user.comfort, model_user.together,
                                                         model_user.fun, model_user.healing, model_user.clean).filter(model_user.access_token == session['access_token']).all()

                        if len(algopoint_query) == 0 or len(userpoint_query) == 0:
                            param['code'] = 500
                            return param
                        else:
                            userpoint_list = [userpoint_query[0].comfort, userpoint_query[0].together, userpoint_query[0].fun,
                                              userpoint_query[0].healing, userpoint_query[0].clean]
                            algopoint_list = [algopoint_query[0].comfort, algopoint_query[0].together, algopoint_query[0].fun,
                                              algopoint_query[0].healing, algopoint_query[0].clean]

                            pa = PolarArea()
                            match_pct = pa.matching_pct(algopoint_list, userpoint_list)
                            match_result.append(match_pct)
                    except:
                        match_result.append('')
                    finally:
                        session_.close()
                return match_result
            else:
                try:
                    '''
                    # SELECT * FROM algopoint WHERE content_id = id;
                    '''
                    algopoint_query = session_.query(model_algopoint.comfort, model_algopoint.together,
                                                     model_algopoint.fun, model_algopoint.healing,
                                                     model_algopoint.clean).filter(
                        model_algopoint.content_id == int(content_id)).all()
                    '''
                    # SELECT comfort, together, fun, healing, clean FROM user WHERE access_token = session['access_token'] 
                    '''
                    userpoint_query = session_.query(model_user.comfort, model_user.together,
                                                     model_user.fun, model_user.healing, model_user.clean).filter(
                        model_user.access_token == session['access_token']).all()

                    if len(algopoint_query) == 0 or len(userpoint_query) == 0:
                        param['code'] = 500
                        return param
                    else:
                        userpoint_list = [userpoint_query[0].comfort, userpoint_query[0].together,
                                          userpoint_query[0].fun,
                                          userpoint_query[0].healing, userpoint_query[0].clean]
                        algopoint_list = [algopoint_query[0].comfort, algopoint_query[0].together,
                                          algopoint_query[0].fun,
                                          algopoint_query[0].healing, algopoint_query[0].clean]

                        pa = PolarArea()
                        match_pct = pa.matching_pct(algopoint_list, userpoint_list)
                except:
                    match_pct = 0
                finally:
                    session_.close()
            return match_pct, userpoint_list
    except:
        return False

# 인기순 정렬
def get_popular_list(place_obj, algo_obj, page):
    place_info = []
    content_id_list = []

    for i, obj in enumerate(place_obj):
        # content_id에 대한 별점, 점수 산출 불가인 경우
        if algo_obj['algo_stars'][i] == '':
            algo_obj['algo_stars'][i] = 0.0
        star = algo_obj['algo_stars'][i]
        tag = algo_obj['tags'][i]

        arr = [obj['place_name'], obj['content_id'], obj['detail_image'],
               obj['tag'], obj['readcount'], str(obj['modified_date']), star, tag]

        place_info.append(arr)
    place_info.sort(key=itemgetter(Config.STAR), reverse=True)  # star = 6

    for info in place_info:
        content_id_list.append(info[1]) # 인기순 정렬된 content_id 리스트

    match_pct = get_matching_rate(content_id_list) if get_matching_rate(content_id_list) else False

    if match_pct is not False:
        match_status = True # ok
        for i, info in enumerate(place_info):
            info.append(match_pct[i])
    else:
        match_status = False # no
    return jsonify(make_resobj(place_info, page, match_status))
 
# 조회순 정렬
def get_readcount_list(place_obj, algo_obj, page):
    place_info = []
    content_id_list = []

    for i, obj in enumerate(place_obj):
        star = algo_obj['algo_stars'][i]
        tag = algo_obj['tags'][i]

        arr = [obj['place_name'], obj['content_id'], obj['detail_image'],
               obj['tag'], obj['readcount'], str(obj['modified_date']), star, tag]

        place_info.append(arr)

    place_info.sort(key=itemgetter(Config.READCOUNT), reverse=True)  # readcount = 4

    for info in place_info:
        content_id_list.append(info[1]) # 조회순 정렬된 content_id 리스트

    match_pct = get_matching_rate(content_id_list) if get_matching_rate(content_id_list) else False

    if match_pct is not False:
        match_status = True  # ok
        for i, info in enumerate(place_info):
            info.append(match_pct[i])
    else:
        match_status = False  # no
    return jsonify(make_resobj(place_info, page, match_status))

# 등록순 정렬
def get_modified_list(place_obj, algo_obj, page):
    place_info = []
    content_id_list = []

    for i, obj in enumerate(place_obj):
        star = algo_obj['algo_stars'][i]
        tag = algo_obj['tags'][i]

        if obj['modified_date'] is None:
            obj['modified_date'] = str('2000-01-01 00:00:00')

        arr = [obj['place_name'], obj['content_id'], obj['detail_image'],
               obj['tag'], obj['readcount'], str(obj['modified_date']), star, tag]

        place_info.append(arr)

    place_info = sorted(place_info,
                        key=lambda x: datetime.datetime.strptime(x[Config.MODIFIED_DATE], '%Y-%m-%d %H:%M:%S'),
                        reverse=True)

    for info in place_info:
        content_id_list.append(info[1]) # 조회순 정렬된 content_id 리스트

    match_pct = get_matching_rate(content_id_list) if get_matching_rate(content_id_list) else False

    if match_pct is not False:
        match_status = True  # ok
        for i, info in enumerate(place_info):
            info.append(match_pct[i])
    else:
        match_status = False  # no
    return jsonify(make_resobj(place_info, page, match_status))

# 알고 점수 호출
def get_score(content_id):
    algostars, algoscores = [], []

    if type(content_id) == list:
        for target_id in content_id:
            star, score = get_algo_points(target_id)
            algostars.append(star)
            algoscores.append(score)
        return algostars, algoscores
    else:
        return get_algo_points(content_id)

# 알고 별점, 알고 점수 계산
def get_algo_points(content_id):
    algo_df = pd.read_csv(Config.ALGO_POINTS)
    try:
        algo_df.set_index(['contentId', 'camp'], inplace=True)
        comfort_point = float(algo_df.loc[content_id]['comfort'])
        together_point = float(algo_df.loc[content_id]['together'])
        fun_point = float(algo_df.loc[content_id]['fun'])
        healing_point = float(algo_df.loc[content_id]['healing'])
        clean_point = float(algo_df.loc[content_id]['clean'])

        cat_points_list = [comfort_point, together_point, fun_point, healing_point, clean_point]
        algo_star = round(sum(cat_points_list) / 100, 1)
    except:
        # content_id에 대한 별점, 점수 산출 불가인 경우
        return 0.0, []
    return algo_star, cat_points_list

# top3,5 특성
def get_top_tag(content_id, num):
    tags = []
    tag = TagPoints()

    if type(content_id) == list:
        for target_id in content_id:
            top3_tag = tag.tag_priority(target_id, rank=num)
            tags.append(top3_tag)
        return tags
    else:
        return tag.tag_priority(content_id, rank=num)

# 반환되는 객체 만들기
def make_resobj(place_info, page, match_status):
    key_list = ['place_name', 'content_id', 'detail_image', 'tag', 'readcount', 'modified_date', 'star', 'tag']

    if match_status:
        key_list.append('match_pct')

    offset = (page * Config.LIMIT_LEN) - Config.LIMIT_LEN

    if page == 1:
        start_page, offset = 0, Config.LIMIT_LEN
    else:
        start_page = page

    params, param_list = {}, []
    stars, tags, match = [], [], []
    for info in place_info:
        param = {key: info[i] for i, key in enumerate(key_list)}
        param_list.append(param)
        stars.append(param['star'])
        tags.append(param['tag'])

        if match_status:
            match.append(param['match_pct'])

    logging.info('----[' + str(datetime.datetime.now()) + ' make_resobj() : 200]----')

    params['code'] = 200
    params['place_info'] = param_list[start_page:offset]
    params['algo_star'] = stars[start_page:offset]
    params['tag'] = tags[start_page:offset]

    if match_status:
        params['match_pct'] = match[start_page:offset]

    return params

# content_id 문자열 리스트(,)에 대한 장소 리스트
def get_placelist(param):
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()

    # access token , content_id 리스트
    if session['access_token'] == param['access_token']:
        try:
            like = param['like']
        except:
            like = param['like[]']

        '''
        # SELECT first_image, place_name FROM place WHERE content_id = param.like[0];
        '''
        res_param = dict()
        try:
            for content_id in like.split(','):
                obj = dict()

                if content_id == 'None' or content_id == '':
                    continue

                query = session_.query(model_place.first_image, model_place.place_name).filter(model_place.content_id == content_id).all()
                obj['first_image'] = str(query[0][0])
                obj['place_name'] = str(query[0][1])
                obj['star'], _ = get_score(int(content_id))
                res_param[content_id] = obj

            res_param['code'] = 200
        except:
            res_param['code'] = 500
        finally:
            session_.close()

        return res_param

# 롤링 배너 시나리오 검색 결과
def get_bannerlist(param):
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()

    scenario_copy = {'s101': '아이들과 가기 좋은 캠핑장', 's102': '동해 근처 캠핑장', 's105': '투어하기 좋은 남해 근처 캠핑장',
                     's108': '가을 정취 가득한 캠핑장', 's111': '반려동물과 함께해서 더 좋은 캠핑장', 's112': '제주 해수욕장 근처 인기 캠핑장',
                     's115': '가족들과 함께 하는 즐거운 오토 캠핑', 's119': '연인과 행복한 글램핑&카라반'}

    try:
        '''
        # SELECT copy, content_id FROM scenario WHERE spot2=1 AND scene_no = param['scene_no'];
        '''
        bannerlist_query = session_.query(model_scenario.copy, model_scenario.content_id).filter(
            and_(model_scenario.spot2 == 1, model_scenario.scene_no == param['scene_no'])
        ).all()

        '''
        # SELECT * FROM place INNER JOIN algopoint ON (place.content_id = algopoint.content_id) WHERE algopoint.content_id = content_id_list[0]
        # UNION ALL SELECT * FROM place INNER JOIN algopoint ON (place.content_id = algopoint.content_id) WHERE algopoint.content_id = content_id_list[1]
        # UNION ALL SELECT * FROM place INNER JOIN algopoint ON (place.content_id = algopoint.content_id) WHERE algopoint.content_id = content_id_list[2]
        # ...
        '''
        content_id_list, copy = list(), ''
        for query in bannerlist_query:
            content_id_list.append(int(query.content_id))
            copy = query.copy

        union_all_query = [session_.query(model_place, model_algopoint).filter(model_place.content_id == model_algopoint.content_id).filter(
            model_place.content_id == content_id
        ) for content_id in content_id_list]

        query = union_all_query[0].union_all(*union_all_query).all()

        res_param, place_info, algostar = dict(), list(), list()
        for q in query:
            place_info.append(q[0])
            algostar.append(q[1].algostar)

        res_param['place_info'] = place_info
        res_param['algostar'] = algostar
        res_param['copy'] = scenario_copy[param['scene_no']]
        res_param['code'] = 200

        logging.info('----[' + str(datetime.datetime.now()) + ' get_bannerlist() : 200]----')
    except:
        logging.error('----[' + str(datetime.datetime.now()) + ' get_bannerlist() : 500]----')
    finally:
        session_.close()
    return jsonify(res_param)

# # content_id에 대한 place info
# def get_searchlist(content_id, copy=None):
#     client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
#     Session = sessionmaker(bind=client)
#     session_ = Session()
#     param = dict()
#     try:
#         '''
#         # SELECT place_name, first_image FROM place WHERE place_num = 0 and content_id = param['content_id'];
#         '''
#         place_query = session_.query(model_place.place_name, model_place.first_image).filter(
#             and_(model_place.place_num == 0, model_place.content_id == content_id)
#         ).all()
#
#         param['place_name'] = place_query[0].place_name
#         param['first_image'] = place_query[0].first_image
#         param['algo_star'], _ = get_score(content_id)
#         param['content_id'] = content_id
#
#         if copy is not None:
#             param['copy'] = copy
#         param['code'] = 200
#
#         logging.info('----[' + str(datetime.datetime.now()) + ' get_searchlist() : 200]----')
#     except:
#         logging.error('----[' + str(datetime.now()) + ' get_searchlist() : 500]----')
#     finally:
#         session_.close()
#     return param
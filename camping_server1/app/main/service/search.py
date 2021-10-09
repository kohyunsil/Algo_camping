from app.main.model.place_dao import PlaceDAO as model_place
from app.main.model.search_dao import SearchDAO as model_search
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

# 검색결과 리스트
def get_searchlist(params, res_len, page):
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
    # SELECT * FROM place WHERE place_num = 0 AND content_id IN(
    # SELECT content_id FROM search WHERE addr LIKE '%지역%' OR place_name LIKE '%캠핑장명%' OR (태그1=1 OR 태그2=1)) ORDER BY (CASE 
    # WHEN place_name LIKE '%캠핑장명%' AND  addr LIKE '%전체%' THEN 1
    # WHEN place_name LIKE '%캠핑장명%' OR addr LIKE '%전체%' THEN 2
    # WHEN addr LIKE '%지역%' THEN 3
    # ELSE 4
    # END) limit 조회할 시작 row, row 개수;
    '''
    Session = sessionmaker(bind=client)
    session_ = Session()

    offset = (page * Config.LIMIT_LEN) - Config.LIMIT_LEN

    try:
        if tag_query == '':
            sub_query = session_.query(model_search.content_id).filter(model_search.addr.like(area) |
                                                                       model_search.place_name.like(place_keyword))
        else:
            sub_query = session_.query(model_search.content_id).filter(model_search.addr.like(area) |
                                                                       model_search.place_name.like(place_keyword) |
                                                                       text(tag_query))

        main_query = session_.query(model_place).filter(
            and_(model_place.place_num == 0, model_place.content_id.in_(sub_query))).order_by(
            case(
                (and_(model_place.place_name.contains(place_keyword), model_place.addr.contains(area)), 1),
                (or_(model_place.place_name.contains(place_keyword), model_place.addr.contains(area)), 2),
                (model_place.addr.contains(area), 3),
                else_=4
            )
        ).offset(offset).limit(Config.LIMIT_LEN).all()

    except:
        params['code'] = 500
    finally:
        session_.close()

    place_info, content_id = [], []
    for query in main_query:
        query.tag = str(query.tag).split('#')[1:4]
        query.detail_image = str(query.detail_image).split(',')[:5]
        content_id.append(query.content_id)
        place_info.append(query)
        query.modified_date = str(query.modified_date)

    algo_stars, algo_scores = get_score(content_id)
    tags = get_top_tag(content_id, 3)

    # setter
    place_dto.place = place_info
    modeling_dto.modeling = {'algo_stars': algo_stars, 'tags': tags}

    logging.info('----[' + str(datetime.datetime.now()) + ' get_searchlist() : 200]----')

    params['code'] = 200
    params['keywords'] = ', '.join(split_params)
    params['res_num'] = len(main_query)
    params['place_info'] = place_info
    params['algo_star'] = algo_stars
    params['algo_score'] = algo_scores
    params['tag'] = tags

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
def get_matching_rate():
    pass

# 인기순 정렬
def get_popular_list(place_obj, algo_obj, page):
    place_info = []

    for i, obj in enumerate(place_obj):
        # content_id에 대한 별점, 점수 산출 불가인 경우
        if algo_obj['algo_stars'][i] == '':
            algo_obj['algo_stars'][i] = 0.0
        star = algo_obj['algo_stars'][i]
        tag = algo_obj['tags'][i]

        arr = [obj.place_name, obj.content_id, obj.detail_image,
               obj.tag, obj.readcount, str(obj.modified_date), star, tag]

        place_info.append(arr)
    place_info.sort(key=itemgetter(Config.STAR), reverse=True)  # star = 6

    return jsonify(make_resobj(place_info, page))
 
# 조회순 정렬
def get_readcount_list(place_obj, algo_obj, page):
    place_info = []

    for i, obj in enumerate(place_obj):
        star = algo_obj['algo_stars'][i]
        tag = algo_obj['tags'][i]

        arr = [obj.place_name, obj.content_id, obj.detail_image,
               obj.tag, obj.readcount, str(obj.modified_date), star, tag]

        place_info.append(arr)

    place_info.sort(key=itemgetter(Config.READCOUNT), reverse=True)  # readcount = 4

    return jsonify(make_resobj(place_info, page))

# 등록순 정렬
def get_modified_list(place_obj, algo_obj, page):
    place_info = []

    for i, obj in enumerate(place_obj):
        star = algo_obj['algo_stars'][i]
        tag = algo_obj['tags'][i]

        if obj.modified_date is None:
            obj.modified_date = str('2000-01-01 00:00:00')

        arr = [obj.place_name, obj.content_id, obj.detail_image,
               obj.tag, obj.readcount, str(obj.modified_date), star, tag]

        place_info.append(arr)

    place_info = sorted(place_info,
                        key=lambda x: datetime.datetime.strptime(x[Config.MODIFIED_DATE], '%Y-%m-%d %H:%M:%S'),
                        reverse=True)

    return jsonify(make_resobj(place_info, page))

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
def make_resobj(place_info, page):
    key_list = ['place_name', 'content_id', 'detail_image', 'tag', 'readcount', 'modified_date', 'star', 'tag']

    offset = (page * Config.LIMIT_LEN) - Config.LIMIT_LEN

    if page == 1:
        start_page, offset = 0, Config.LIMIT_LEN
    else:
        start_page = page

    params, param_list = {}, []
    stars, tags = [], []
    for info in place_info:
        param = {key: info[i] for i, key in enumerate(key_list)}
        param_list.append(param)
        stars.append(param['star'])
        tags.append(param['tag'])

    logging.info('----[' + str(datetime.datetime.now()) + ' make_resobj() : 200]----')

    params['code'] = 200
    params['place_info'] = param_list[start_page:offset]
    params['algo_star'] = stars[start_page:offset]
    params['tag'] = tags[start_page:offset]

    return params
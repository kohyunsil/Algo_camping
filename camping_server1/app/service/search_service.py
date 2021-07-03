from ..model.place_dao import PlaceDAO as model_place
from ..model.search_dao import SearchDAO as model_search
from ..model import *
from sqlalchemy.orm import sessionmaker
from flask import *
from operator import itemgetter
from ..config import Config
from datetime import datetime

def get_searchlist(params):
    split_params = []

    for param in params['keywords'].split(';'):
        if param != '':
            split_params.append(param)

    place_keyword, area = '', ''
    category_keyword = []

    # 입력 데이터 태그/캠핑장 구분
    for i, param in enumerate(split_params):
        if i == 0:
            if split_params[0] == '전체':
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

        if category_keyword[len(category_keyword) -1] == tag:
            tag_query += ' = 1'
        else:
            tag_query += ' = 1 or '

    '''
    # select * from place where content_id in(
    # select content_id from search where addr like '%지역%' or place_name like '%캠핑장명%' or (태그=1 or 태그=1)) order by (case 
    # when place_name like '%캠핑장명%' then 1
    # when addr like '%지역%' then 2
    # else 3
    # end);
    '''
    Session = sessionmaker(bind=client)
    session_ = Session()

    if tag_query == '':
        sub_query = session_.query(model_search.content_id).filter(model_search.addr.like(area) |
                                                                   model_search.place_name.like(place_keyword)).subquery()
    else:
        sub_query = session_.query(model_search.content_id).filter(model_search.addr.like(area) |
                                                                   model_search.place_name.like(place_keyword) |
                                                                   text(tag_query)).subquery()

    main_query = session_.query(model_place).filter(model_place.content_id.in_(sub_query)).order_by(
        case(
            (model_place.place_name.like(place_keyword), 1),
            (model_place.addr.like(area), 2),
            else_=3
        )
    ).limit(Config.LIMIT).all()

    place_info = []
    for query in main_query:
        query.tag = str(query.tag).split('#')[1:4]
        query.detail_image = str(query.detail_image).split(',')[:]
        place_info.append(query)

    # setter
    dto.place = place_info

    params['code'] = 200
    params['keywords'] = ', '.join(split_params)
    params['res_num'] = len(main_query)
    params['place_info'] = place_info

    return params

def get_readcount_list(place_obj):
    place_info = []

    for i in range(len(place_obj)):
        arr = [place_obj[i].place_name, place_obj[i].content_id, place_obj[i].detail_image,
               place_obj[i].tag, place_obj[i].readcount]

        place_info.append(arr)

    # 인기순 정렬
    place_info.sort(key=itemgetter(Config.READCOUNT), reverse=True) # readcount = 4
    key_list = ['place_name', 'content_id', 'detail_image', 'tag', 'readcount']

    params, param_list = {}, []
    for info in place_info:
        param = {key: info[i] for i, key in enumerate(key_list)}
        param_list.append(param)

    params['code'] = 200
    params['place_info'] = param_list

    return jsonify(params)

def get_modified_list(place_obj):
    place_info = []

    for i in range(len(place_obj)):
        if place_obj[i].modified_date is None:
            place_obj[i].modified_date = str('2000-01-01 00:00:00')

        arr = [place_obj[i].place_name, place_obj[i].content_id, place_obj[i].detail_image,
               place_obj[i].tag, place_obj[i].readcount, str(place_obj[i].modified_date)]

        place_info.append(arr)

    # 등록일 기준 정렬
    place_info = sorted(place_info, key=lambda x: datetime.strptime(x[Config.MODIFIED_DATE], '%Y-%m-%d %H:%M:%S'),
                        reverse=True)

    key_list = ['place_name', 'content_id', 'detail_image', 'tag', 'readcount', 'modified_date']

    params, param_list = {}, []
    for info in place_info:
        param = {key: info[i] for i, key in enumerate(key_list)}
        param_list.append(param)

    params['code'] = 200
    params['place_info'] = param_list
    return jsonify(params)
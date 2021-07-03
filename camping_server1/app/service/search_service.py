from ..model.place_dao import PlaceDAO as model_place
from ..model.search_dao import SearchDAO as model_search
from ..model import *
from sqlalchemy.orm import sessionmaker

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
        tag_query += (getattr(model_search, tag) == 1)

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

    sub_query = session_.query(model_search.content_id).filter(model_search.addr.like(area) |
                                                               model_search.place_name.like(place_keyword) |
                                                               tag_query).subquery()
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
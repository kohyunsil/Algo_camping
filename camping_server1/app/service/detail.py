from ..model.review_dao import ReviewDAO as model_review
from ..model.congestion_dao import CongestionDAO as model_congestion
from ..model.place_dao import PlaceDAO as model_place
from ..model import *
from ..service.search import get_score, get_top_tag
from sqlalchemy.orm import sessionmaker
from flask import *
from ..config import Config
import datetime

# 상세 정보
def get_detail(param):
    if len(param) == 0 or str(list(param.keys())[0]) != 'content_id':
        return redirect('/main', code=302)

    else:
        req_contentid = param['content_id']
        params = {}

        '''
        # select avg(star) from review where place_id in(
        # select id from place where content_id = 특정 장소의 content_id);
        '''
        Session = sessionmaker(bind=client)
        session_ = Session()

        if req_contentid is not None:
            place_info = session_.query(model_place).filter(model_place.content_id == int(req_contentid)).all()
            id = place_info[0].id

            review_query = model_review.query.with_entities(func.avg(model_review.star).label('avg_star')).filter(model_review.place_id == id).all()

            if review_query[0][0] is None:
                avg_star = 0
            else:
                avg_star = round(float(review_query[0][0]), 2)

            local_obj = get_local(place_info[0].sigungu_code)
            past_congestion_obj = get_past_congestion(place_info[0].content_id)
            # future_congestion_obj = get_future_congestion(place_info[0].sigungu_code)
            # future_date, future_congestion = json_default(future_congestion_obj)

            params['place_info'] = place_info[0]
            params['avg_star'] = avg_star
            params['local_info'] = local_obj if local_obj is not None else None

            params['past_congestion'] = past_congestion_obj if past_congestion_obj is not None else None
            # params['future_date'] = future_date
            # params['future_congestion'] = future_congestion

            params['algo_star'], params['algo_score'] = get_score(place_info[0].content_id)
            params['tag'] = get_top_tag(int(req_contentid), 5)

            try:
                params['user_name'] = session['name']
            except KeyError:
                params['user_name'] = '사용자'
        params['code'] = 200
    return jsonify(params)

# 관광지, 축제 정보
def get_local(sigungu_code):
    if sigungu_code is not None:
        Session = sessionmaker(bind=client)
        session_ = Session()
        '''
        # select * from place where (place_num = 1 or place_num = 2 )
        # and sigungu_code = 47130 order by readcount desc limit 5;
        '''
        query = session_.query(model_place).filter(or_(model_place.place_num == 1, model_place.place_num == 2) &
                                                   (model_place.sigungu_code == int(sigungu_code))
                                                   ).order_by(model_place.readcount.desc()).limit(Config.LIMIT).all()
        return query
    else:
        return None

# 과거 혼잡도
def get_past_congestion(content_id):
    if content_id is not None:
        base = datetime.datetime.today().strftime('%Y-%m-%d 00:00:00')
        past = (datetime.datetime.now() - datetime.timedelta(days=Config.DATE_RANGE)).strftime('%Y-%m-%d 00:00:00')

        Session = sessionmaker(bind=client)
        session_ = Session()

        '''
        # select * from congestion where base_ymd between date('과거일') and date('현재일')+1 and content_id=특정 content_id
        # order by base_ymd;
        '''
        query = model_congestion.query.filter(model_congestion.base_ymd.between(past, base) + 1,
                                                 model_congestion.content_id == int(content_id)).all()

        return query

# 미래 혼잡도
def get_future_congestion(sigungu_code):
    if sigungu_code is not None:
        base = datetime.datetime.today().strftime('%Y-%m-%d 00:00:00')
        future = (datetime.datetime.now() + datetime.timedelta(days=Config.DATE_RANGE)).strftime('%Y-%m-%d 00:00:00')

        Session = sessionmaker(bind=client)
        session_ = Session()

        '''
        # select base_ymd, avg(congestion) as congestion from congestion where base_ymd 
        between date('현재일') and date('미래일') and sigungu_code = 시군구코드 group by base_ymd;
        '''
        query = session_.query(model_congestion.base_ymd, func.avg(model_congestion.congestion).label('congestion')).filter(
            model_congestion.base_ymd.between(base, future), model_congestion.sigungu_code == int(sigungu_code)
        ).group_by(model_congestion.base_ymd).all()

        return query
    else:
        return None

# json serialize date to str
def json_default(query_obj):
    date, congestion = [], []
    for obj in query_obj:
        parse = str(obj.base_ymd).split(' 00:00:00')[0]
        date.append(parse)

        future_congestion = float(obj.congestion)
        congestion.append(future_congestion)

    return date, congestion
from ..model.review_dao import ReviewDAO as model_review
from ..model.congestion_dao import CongestionDAO as model_congestion
from ..model.place_dao import PlaceDAO as model_place
from ..model import *
from ..service.search import get_score
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
            congestion_obj = get_past_congestion(place_info[0].content_id)

            params['place_info'] = place_info[0]
            params['avg_star'] = avg_star
            params['local_info'] = local_obj if local_obj is not None else None
            params['congestion'] = congestion_obj if congestion_obj is not None else None
            params['algo_star'], params['algo_score'] = get_score(place_info[0].content_id)

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
        # select * from congestion where base_ymd between date('과거일') and date('현재일')+1 and content_id=39 
        # order by base_ymd;
        '''
        query = model_congestion.query.filter(model_congestion.base_ymd.between(past, base) + 1,
                                                 model_congestion.content_id == int(content_id)).all()

        return query

# 미래 혼잡도 예측
def get_future_congestion(content_id):
    if content_id is not None:

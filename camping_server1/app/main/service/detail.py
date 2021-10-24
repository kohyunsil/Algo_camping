from app.main.model.review_dao import ReviewDAO as model_review
from app.main.model.congestion_dao import CongestionDAO as model_congestion
from app.main.model.place_dao import PlaceDAO as model_place
from app.main.model import *
from ..service.search import get_score, get_top_tag, get_matching_rate
from ..service.user import get_likelist
from sqlalchemy.orm import sessionmaker
from flask import *
import pandas as pd
from app.config import Config
from .congestion import Visitor
import datetime
import logging

# 상세 정보
def get_detail(param):
    if len(param) == 0 or str(list(param.keys())[0]) != 'content_id':
        return redirect('/main', code=302)

    else:
        req_contentid = param['content_id']
        params = {}
        '''
        # SELECT AVG(star) FROM review WHERE place_id IN(
        # SELECT id FROM place WHERE content_id = 특정 장소의 content_id);
        '''
        Session = sessionmaker(bind=client)
        session_ = Session()

        try:
            if req_contentid is not None:
                place_info = session_.query(model_place).filter(model_place.content_id == int(req_contentid)).all()

                review_query = model_review.query.with_entities(func.avg(model_review.star).label('avg_star')).filter(
                    model_review.place_id == req_contentid).all()

                if review_query[0][0] is None:
                    avg_star = 0
                else:
                    avg_star = round(float(review_query[0][0]), 2)

                local_obj = get_local(place_info[0].sigungu_code)

                congestion_obj = get_congestion(place_info[0].sigungu_code)
                params['congestion_obj'] = congestion_obj

                params['place_info'] = place_info[0]
                params['place_info'].detail_image = str(place_info[0].detail_image).split(',')[:5]

                params['avg_star'] = avg_star
                params['local_info'] = local_obj if local_obj is not None else None

                params['algo_star'], params['algo_score'] = get_score(place_info[0].content_id)
                params['tag'] = get_top_tag(int(req_contentid), 5)

                try:
                    params['user_name'] = session['name']
                except KeyError:
                    params['user_name'] = '사용자'

            logging.info('----[' + str(datetime.datetime.now()) + ' get_detail() : 200]----')
            params['code'] = 200

            # 비로그인 시 x
            try:
                if session['access_token']:
                    params['like'] = get_likelist()['like']
                    params['match_pct'], params['user_point'] = get_matching_rate(int(req_contentid))
            except:
                pass
            finally:
                session_.close()

        except:
            logging.error('----[' + str(datetime.datetime.now()) + ' get_detail() : 500]----')
            params['code'] = 500
        finally:
            session_.close()

    return jsonify(params)

# 관광지, 축제 정보
def get_local(sigungu_code):
    Session = sessionmaker(bind=client)
    session_ = Session()

    try:
        if sigungu_code is not None:
            '''
            # SELECT * FROM place WHERE (place_num = 1 OR place_num = 2 )
            # AND sigungu_code = 47130 ORDER BY readcount DESC LIMIT 5;
            '''
            query = session_.query(model_place).filter(or_(model_place.place_num == 1, model_place.place_num == 2) &
                                                       (model_place.sigungu_code == int(sigungu_code))
                                                       ).order_by(model_place.readcount.desc()).limit(Config.LIMIT).all()
            return query
        else:
            return None
    except:
        pass
    finally:
        session_.close()

# 과거 혼잡도
def get_past_congestion(content_id):
    Session = sessionmaker(bind=client)
    session_ = Session()
    try:
        if content_id is not None:
            base = datetime.datetime.today().strftime('%Y-%m-%d 00:00:00')
            past = (datetime.datetime.now() - datetime.timedelta(days=Config.DATE_RANGE)).strftime('%Y-%m-%d 00:00:00')

            '''
            # SELECT * FROM congestion WHERE base_ymd BETWEEN date('과거일') AND date('현재일')+1 AND content_id=특정 content_id
            # ORDER BY base_ymd;
            '''
            query = model_congestion.query.filter(model_congestion.base_ymd.between(past, base) + 1,
                                                  model_congestion.content_id == int(content_id)).all()

            return query
        else:
            return None
    except:
        pass
    finally:
        session_.close()

# 혼잡도 (시군구, 전체 지역 평균)
def get_congestion(sigungu_code):
    param = dict()
    vs = Visitor()

    final_df = vs.visitor_final(int(sigungu_code))
    final_df.index = final_df.index.map(str)

    base_ymd = final_df.index.tolist()
    avg_visitor = pd.to_numeric(final_df['avg_visitor']).values.tolist()
    avg_visitor = [val * 10 for val in avg_visitor]
    sgg_visitor = pd.to_numeric(final_df['sgg_visitor']).values.tolist()

    param['base_ymd'] = base_ymd
    param['avg_visitor'] = avg_visitor
    param['sgg_visitor'] = sgg_visitor

    return param

# json serialize date to str
def json_default(query_obj):
    date, congestion = [], []
    for obj in query_obj:
        parse = str(obj.base_ymd).split(' 00:00:00')[0]
        date.append(parse)

        future_congestion = float(obj.congestion)
        congestion.append(future_congestion)

    return date, congestion
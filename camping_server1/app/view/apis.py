from flask import *
from ..model.place_dao import PlaceDAO as model_place
from ..model.search_dao import SearchDAO as model_search
from ..view import *
from ..model import *


@app.route('/')
@app.route('/main')
def main_page():
    return make_response(render_template('index.html'))


# select tag request
@app.route('/place/<keywords>', methods=['GET'])
def search_place(keywords):
    return jsonify({'abc': keywords})


# url param이 유효하면 이동, 유효하지 않으면 main으로 이동
@app.route('/search')
@app.route('/searchlist')
def search_tags():
    params = request.args.to_dict()
    split_params = []

    if len(params) == 0 or str(list(params.keys())[0]) != 'keywords':
        print(str(params.keys()))
        return redirect('/main', code=302)
    else:
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
        # select content_id from search where addr like '%지역%' or place_name like '%캠핑장 관련 키워드%'  or (태그=1 or 태그=1) ) order by content_id asc;
        '''
        sub_query = session_.query(model_search.content_id).filter(model_search.addr.like(area) |
                                                                   model_search.place_name.like(place_keyword) |
                                                                   tag_query).subquery()
        main_query = session_.query(model_place).filter(model_place.content_id.in_(sub_query)).order_by(model_place.content_id.asc()).all()
        # print(main_query)
        # session_.commit()


        place_info = []
        for query in main_query:
            query.tag = str(query.tag).split('#')[1:4]
            query.detail_image = str(query.detail_image).split(',')[:]
            place_info.append(query)

        return render_template('searchlist.html', keywords=', '.join(split_params), res_num=len(main_query), place_info=place_info)

from flask import *
from ..model import *
from ..service import search_service

@app.route('/')
@app.route('/main')
def main_page():
    return make_response(render_template('index.html'))

# url param이 유효하면 이동, 유효하지 않으면 main으로 이동
# 검색 결과 리스트
@app.route('/searchlist')
def search_tags():
    params = request.args.to_dict()

    if len(params) == 0 or str(list(params.keys())[0]) != 'keywords':
        print(str(params.keys()))
        return redirect('/main', code=302)
    else:
        return search_service.get_searchlist(params)

# 인기순 정렬
@app.route('/search/popular')
def search_popular():
    # getter
    place_obj = dto.place

    return search_service.get_readcount_list(place_obj)

# 조회순 정렬
@app.route('/search/readcount')
def search_readcount():
    # getter
    place_obj = dto.place

    return search_service.get_readcount_list(place_obj)

# 등록순 정렬
@app.route('/search/recent')
def search_recent():
    # getter
    place_obj = dto.place

    return search_service.get_modified_list(place_obj)

# 상세 페이지
@app.route('/detail/info')
def detail_info():
    param = request.args.to_dict()

    return search_service.get_detail(param)
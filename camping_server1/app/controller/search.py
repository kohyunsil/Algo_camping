from app import *
from ..service import search
from ..model import *

# 검색 결과 리스트
@app.route('/search/list')
def search_tags():
    params = request.args.to_dict()

    if len(params) == 0 or str(list(params.keys())[0]) != 'keywords':
        return redirect('/main', code=302)
    else:
        return search.get_searchlist(params)

# 인기순 정렬
@app.route('/search/popular')
def search_popular():
    # getter
    place_obj = place_dto.place
    algo_obj = modeling_dto.modeling
    return search.get_popular_list(place_obj, algo_obj)

# 조회순 정렬
@app.route('/search/readcount')
def search_readcount():
    # getter
    place_obj = place_dto.place
    algo_obj = modeling_dto.modeling
    return search.get_readcount_list(place_obj, algo_obj)

# 등록순 정렬
@app.route('/search/recent')
def search_recent():
    # getter
    place_obj = place_dto.place
    algo_obj = modeling_dto.modeling
    return search.get_modified_list(place_obj, algo_obj)
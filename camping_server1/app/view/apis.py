from flask import *
from ..model.place_dao import PlaceDAO as model_place
from ..model.search_dao import SearchDAO as model_search
from ..model import *
from ..service import search_service
from ..util import place_dto
from ..config import Config
from operator import itemgetter

@app.route('/')
@app.route('/main')
def main_page():
    return make_response(render_template('index.html'))

# url param이 유효하면 이동, 유효하지 않으면 main으로 이동
@app.route('/searchlist')
def search_tags():
    params = request.args.to_dict()

    if len(params) == 0 or str(list(params.keys())[0]) != 'keywords':
        print(str(params.keys()))
        return redirect('/main', code=302)
    else:
        return search_service.get_searchlist(params)

@app.route('/search/popular')
def search_popular():
    # getter
    place_obj = dto.place

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
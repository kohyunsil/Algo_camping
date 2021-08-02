from app.main.service import search as search_service
from app.main.model import *
from flask_restx import Resource, Namespace
from flask import request, redirect, jsonify

search = Namespace('search', description='relating to search')


@search.route('/list')
class SearchTags(Resource):
    def get(self):
        """전체 검색 결과 리스트"""
        params = request.args.to_dict()
        if len(params) == 0 or str(list(params.keys())[0]) != 'keywords':
            return redirect('/main', code=302)
        else:
            return jsonify(search_service.get_searchlist(params))


@search.route('/popular')
class SearchPopular(Resource):
    def get(self):
        """인기순 정렬"""
        # getter
        place_obj = place_dto.place
        algo_obj = modeling_dto.modeling
        return search_service.get_popular_list(place_obj, algo_obj)


@search.route('/readcount')
class SearchReadCount(Resource):
    def get(self):
        """조회순 정렬"""
        # getter
        place_obj = place_dto.place
        algo_obj = modeling_dto.modeling
        return search_service.get_readcount_list(place_obj, algo_obj)


@search.route('/recent')
class SearchRecent(Resource):
    def get(self):
        """등록순 정렬"""
        # getter
        place_obj = place_dto.place
        algo_obj = modeling_dto.modeling
        return search_service.get_modified_list(place_obj, algo_obj)
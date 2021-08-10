from app.main.service import search as search_service
from app.main.model import *
from flask_restx import Resource, Namespace, fields
from flask import request, redirect, jsonify

search = Namespace('search', description='relating to search')

place_obj = search.model('Place Object Resource Fields',
                         {'place_name': fields.String(required=False,
                                                      description='place name'),
                          'detail_image': fields.List(fields.String(required=False),
                                                      description='place num (0 | 1 | 2)'),
                          'content_id': fields.Integer(required=True,
                                                       description='place api unique id'),
                          'readcount': fields.Integer(required=False,
                                                      description='place read count')
                          })
search_model = search.model('Response Search Model',
                            {'keywords': fields.String(required=False,
                                                       description='user requested keywords'),
                             'res_num': fields.Integer(required=False,
                                                       description='response data length'),
                             'place_info': fields.List(fields.Nested(place_obj)),
                             'algo_score': fields.List(fields.List(fields.Integer(required=False)),
                                                       description='algo score for each place'),
                             'algo_star': fields.List(fields.Integer,
                                                      required=False,
                                                      description='algo star for each place'),
                             'tag': fields.List(fields.List(fields.String(required=False)),
                                                description='algo top tags for each place'),
                             })


@search.route('/list')
@search.doc(params={'keywords': '검색 요청 태그 ex);지역;사용자 입력 검색 태그1;사용자 입력 검색 태그2; .. '})
@search.doc(responses={400: 'Validation Error', 500: 'Database Server Error'})
@search.response(200, 'Success', search_model)
class SearchTags(Resource):
    def get(self):
        """전체 검색 결과 리스트"""
        params = request.args.to_dict()
        if len(params) == 0 or str(list(params.keys())[0]) != 'keywords':
            return redirect('/main', code=302)
        else:
            return jsonify(search_service.get_searchlist(params))


@search.route('/popular')
@search.response(200, 'Success', search_model)
class SearchPopular(Resource):
    def get(self):
        """인기순 정렬"""
        # getter
        place_obj = place_dto.place
        algo_obj = modeling_dto.modeling
        return search_service.get_popular_list(place_obj, algo_obj)


@search.route('/readcount')
@search.response(200, 'Success', search_model)
class SearchReadCount(Resource):
    def get(self):
        """조회순 정렬"""
        # getter
        place_obj = place_dto.place
        algo_obj = modeling_dto.modeling
        return search_service.get_readcount_list(place_obj, algo_obj)


@search.route('/recent')
@search.response(200, 'Success', search_model)
class SearchRecent(Resource):
    def get(self):
        """등록순 정렬"""
        # getter
        place_obj = place_dto.place
        algo_obj = modeling_dto.modeling
        return search_service.get_modified_list(place_obj, algo_obj)

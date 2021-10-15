from app.main.service import search as search_service
from app.main.service import main as main_service
from app.main.model import *
from flask_restx import Resource, Namespace, fields
from flask import request, redirect, jsonify
import logging

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

keyword_list = []

@search.route('/pagination/<string:sort_type>/<int:res_len>/<int:page>')
@search.param('sort_type', '정렬 방식')
@search.param('res_len', '검색 결과 개수')
@search.param('page', '요청 페이지')
@search.doc(responses={400: 'Validation Error', 500: 'Database Server Error'})
@search.response(200, 'Success', search_model)
class SearchPagination(Resource):
    def get(self, sort_type, res_len, page):
        """페이지네이션"""
        params = request.args.to_dict()

        if len(params) == 0 or str(list(params.keys())[0]) != 'keywords':
            return redirect('/main', code=302)
        else:
            headers = str(request.headers)
            base_url = request.base_url
            screen = request.path
            method = request.method
            action = 'click'
            if page == 1:
                type = 'search'
            else:
                type = 'pagination'
            keyword = params['keywords'].split(';')[1:]

            main_service.user_event_logging(headers, base_url, screen, method, action, type, keyword, page=page)

            if sort_type in ['popular', 'readcount', 'recent']:
                # getter
                place_obj = place_dto.place
                algo_obj = modeling_dto.modeling

                if sort_type == 'popular':
                    return search_service.get_popular_list(place_obj, algo_obj, page)
                elif sort_type == 'readcount':
                    return search_service.get_readcount_list(place_obj, algo_obj, page)
                elif sort_type == 'recent':
                    return search_service.get_modified_list(place_obj, algo_obj, page)

        return jsonify(search_service.get_searchlist(params, res_len, page))


@search.route('/list')
@search.doc(params={'keywords': '검색 요청 태그 ex);지역;사용자 입력 검색 태그1;사용자 입력 검색 태그2; .. '})
@search.doc(responses={400: 'Validation Error', 500: 'Database Server Error'})
@search.response(200, 'Success', search_model)
class SearchTags(Resource):
    def get(self):
        """전체 검색 수"""
        params = request.args.to_dict()
        return search_service.get_row_nums(params)


@search.route('/likelist')
@search.doc(params={'content_id_list': 'content_id 리스트', 'access_token': 'access token'})
@search.doc(responses={400: 'Validation Error', 500: 'Database Server Error'})
@search.response(200, 'Success', search_model)
class SearchTags(Resource):
    def get(self):
        """content_id 리스트에 대한 장소 리스트"""
        params = request.args.to_dict()
        return search_service.get_placelist(params)
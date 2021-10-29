from app.main.service import detail as detail_service
from app.main.service import main as main_service
from app.main.service import user as user_service
from flask_restx import Resource, Namespace, fields
from flask import request

detail = Namespace('detail', description='relating to detail')

local_obj = detail.model('Local Place & Festival Object Resource Fields',
                         {'place_name': fields.String(required=False,
                                                      description='place name'),
                          'addr': fields.String(required=False,
                                                description='place address'),
                          'first_image': fields.String(required=False,
                                                       description='place first image')
                          })
congestion_obj = detail.model('Specific Sigungu Past Congestion Object Resource Fields',
                              {'base_ymd': fields.String(required=False,
                                                         description='specific sigungu congestion base date'),
                               'congestion': fields.Float(required=False,
                                                          description='specific sigungu visit num'),
                               'content_id': fields.Integer(required=False,
                                                            description='specific sigungu place content id')
                               })
place_obj = detail.model('Specific Place Object Resource Fields',
                         {'place_name': fields.String(required=False,
                                                      description='specific camping place name'),
                          'line_intro': fields.String(required=False,
                                                      description='specific camping place line intro'),
                          'addr': fields.String(required=False,
                                                description='specific camping place address'),
                          'lat': fields.Float(required=False,
                                              description='specific camping place latitude'),
                          'lng': fields.Float(required=False,
                                              description='specific camping place longitude'),
                          'oper_date': fields.String(required=False,
                                                     description='specific camping place operation date'),
                          'industry': fields.String(required=False,
                                                    description='specific camping place industry'),
                          'homepage': fields.String(required=False,
                                                    description='specific camping place homepage url'),
                          'tel': fields.String(required=False,
                                               description='specific camping place tel'),
                          'detail_image': fields.List(fields.String(required=False,
                                                                    description='specific camping place detail images'))
                          })

place_model = detail.model('Specific Place Model',
                           {'place_info': fields.Nested(place_obj),
                            'avg_star': fields.Float(required=False,
                                                     description='specific place visitor average star'),
                            'local_info': fields.Nested(local_obj),
                            'past_congestion': fields.Nested(congestion_obj),
                            'algo_star': fields.Float(required=False,
                                                      description='specific place algo star'),
                            'algo_score': fields.List(fields.Float(required=False,
                                                                   description='specific place algo scores')),
                            'tag': fields.List(fields.String(required=False,
                                                             description='specific place top tags')),
                            'user_name': fields.String(required=False,
                                                       description='user name')})

@detail.route('/info')
@detail.doc(responses={302: 'redirect'})
@detail.response(200, 'Success', place_model)
class DetailAll(Resource):
    def get(self):
        """상세 내용"""
        param = request.args.to_dict()

        headers = str(request.headers)
        base_url = request.base_url
        screen = request.path
        method = request.method
        action = 'click'
        type = 'card'
        keyword = []

        main_service.user_event_logging(headers, base_url, screen, method, action, type, keyword, param)

        return detail_service.get_detail(param)
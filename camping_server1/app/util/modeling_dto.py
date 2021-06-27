from flask_restx import Namespace, fields


class ModelingDTO:
    api = Namespace('tag', description='relating to algorithm tag')
    tag = api.model('api', {
        'place_name': fields.String(required=False),
        'addr': fields.String(required=False),
        'main_cat': fields.String(required=False),
        'sub_cat': fields.String(required=False),
        'weight': fields.Integer(required=False)
    })

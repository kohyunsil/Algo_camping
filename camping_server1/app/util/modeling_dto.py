from flask_restx import Namespace, fields


class ModelingDTO:
    api = Namespace('modeling', description='relating to algorithm tag')
    modeling = api.model('api', {
        'place_name': fields.String(required=False),
        'content_id': fields.Integer(required=False),
        'addr': fields.String(required=False),
        'cat': fields.String(required=False),
        'weight': fields.Integer(required=False)
    })

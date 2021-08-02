from flask_restx import Namespace, fields


class UserDTO:
    api = Namespace('user', description='relating to user')
    user = api.model('user', {
        'user_name': fields.String(required=False),
        'email': fields.String(required=False),
    })
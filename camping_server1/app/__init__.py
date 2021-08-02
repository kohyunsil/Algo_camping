from flask_restx import Api
from flask import Blueprint
from .main.controller.user import user
from .main.controller.search import search
from .main.controller.detail import detail

blueprint = Blueprint('api', __name__, static_folder='static', template_folder='templates')

api = Api(blueprint,
          version='1.0',
          title='AlgoCamping API server',
          description='algocamping api server description',
          doc='/doc')

api.add_namespace(user, path='/user')
api.add_namespace(search, path='/search')
api.add_namespace(detail, path='/detail')
from flask import Flask
from flask import *
from flask_mongoengine import MongoEngine
import logging
from logging.config import dictConfig
from ..view import routes
from app.main.controller import user
import warnings
from ..config import DBConfig, Config
from datetime import datetime
from .model import db, migrate
from flask_jwt_extended import *


warnings.filterwarnings('ignore')

def create_app():
    app = Flask(__name__, static_folder=None)

    # register route
    app.register_blueprint(routes.route_api)
    app.register_blueprint(user.auth)

    app.config.from_object(DBConfig)
    db.init_app(app)
    migrate.init_app(app, db)

    mongodb = MongoEngine()

    jwt = JWTManager(app)

    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://' + DBConfig.MONGO_USER + ':' + DBConfig.MONGO_PWD + '@' + DBConfig.MONGO_HOST + ':27017/' + DBConfig.MONGO_DB + '?authSource=admin'
    }

    mongodb.init_app(app)
    migrate.init_app(app, mongodb)

    app.config.update(
        DEBUG=True,
        JWT_SECRET_KEY=Config.JWT_SECRET_KEY
    )

    logging_format = '%(asctime)s - %(levelname)s - %(message)s'

    # logging.basicConfig(filename=str(datetime.now()) + '_debug.log', level=logging.DEBUG, format=logging_format)
    logging.basicConfig(filename=str(datetime.now()) + '_warn.log', level=logging.WARN, format=logging_format)
    logging.basicConfig(filename=str(datetime.now()) + '_warning.log', level=logging.WARNING, format=logging_format)
    logging.basicConfig(filename=str(datetime.now()) + '_error.log', level=logging.ERROR, format=logging_format)

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format' : "%(asctime)s | %(lineno)d line | %(funcName)s() | %(levelname)s | %(message)s "
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })
    return app
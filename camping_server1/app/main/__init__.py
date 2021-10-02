from flask import Flask
from flask import *
import logging
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

    app.config.update(
        DEBUG=True,
        JWT_SECRET_KEY=Config.JWT_SECRET_KEY
    )

    jwt = JWTManager(app)

    logging_format = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=str(datetime.now()) + 'log/debug/_debug.log', level=logging.DEBUG, format=logging_format)
    logging.basicConfig(filename=str(datetime.now()) + 'log/warning/_warning.log', level=logging.WARNING, format=logging_format)
    logging.basicConfig(filename=str(datetime.now()) + 'log/error/_error.log', level=logging.ERROR, format=logging_format)

    return app
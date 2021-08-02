from flask import Flask
from ..view import routes
from app.main.controller import user
import warnings
from ..config import DBConfig
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

    jwt = JWTManager(app)

    return app
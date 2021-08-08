from flask import Flask
from ..view import routes
from app.main.controller import user
import warnings
from ..config import DBConfig, Config
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

    return app
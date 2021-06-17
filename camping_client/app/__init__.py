from flask import *
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.views import routes

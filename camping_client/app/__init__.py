from flask import *
import os

from camping_client.app.config import Config
from camping_client.app.views import routes

app = Flask(__name__)
app.config.from_object(Config)



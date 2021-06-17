import os

class Config(object):
    TEMPLATE_AUTO_RELOAD = True
    BASE_PATH = os.path.dirname(os.path.dirname(__file__))
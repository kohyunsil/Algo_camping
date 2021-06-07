import configparser
import os

config = configparser.RawConfigParser()
abspath = os.path.abspath('../keys/data.ini')
config.read(abspath)
keys = config['API_KEYS']

class Config:
    PATH = os.path.abspath('../../datas')
    config.read(PATH)
    MAX_PAGE = 100  # naver v4 max page
    PUBLIC_API_KEY = keys['PUBLIC_API_KEY']

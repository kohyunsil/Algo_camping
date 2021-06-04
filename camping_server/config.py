import configparser

config = configparser.RawConfigParser()
config.read('./keys/data.ini')
keys = config['API_KEYS']

class Config():
    PATH = '../../datas/'
    MAX_PAGE = 100  # naver v4 max page
    PUBLIC_API_KEY = keys['PUBLIC_API_KEY']
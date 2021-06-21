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
    COUNT = 100 # naver v5 review max count
    SCROLL_NUM = 10 # naver v5 scroll count
    WEBHOOK_URL = keys['WEBHOOK_URL'] # slack webhook url
    DO_LIST = {'충북': '충청북도', '충남': '충청남도',
               '경북': '경상북도', '경남': '경상남도',
               '전북': '전라북도', '전남': '전라남도',
               '강원': '강원도', '경기': '경기도',
               '인천': '인천광역시', '인천시': '인천광역시',
               '부산': '부산광역시', '울산': '울산광역시', '대전': '대전광역시',
               '대구': '대구광역시', '광주': '광주광역시',
               '서울': '서울특별시', '서울시': '서울특별시',
               '제주': '제주특별자치도', '제주도': '제주특별자치도'}
import configparser
import pandas as pd
import datetime
import os

config = configparser.ConfigParser()
abspath = os.path.abspath('data.ini')
config.read(abspath)
keys = config['SECRET_KEYS']
mongo_keys = config['MONGODB']
aws_s3 = config['S3']
kakao = config['KAKAO']


class DBConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'super secret key'

    DB = keys['DB']
    HOST = keys['HOST']
    PASSWORD = keys['PASSWORD']
    
    SQLALCHEMY_DATABASE_URI = (
            'mysql://root:' + keys['PASSWORD'] + '@' + keys['HOST'] + ':3306/' + keys['DB'] + '?charset=utf8'
        # 'mysql://root:root@localhost:3306/camping?charset=utf8'
    )
    # MONGO_DATABASE_URI = 'mongodb://' + mongo_keys['USER'] + ':' + mongo_keys['PASSWORD'] + '@' + mongo_keys['HOST'] + ':27017/'
    MONGO_USER = mongo_keys['USER']
    MONGO_PWD = mongo_keys['PASSWORD']
    MONGO_HOST = mongo_keys['HOST']
    MONGO_DB = mongo_keys['DB']

class Config(object):
    TEMPLATE_AUTO_RELOAD = True

    AWS_ACCESS_KEY = aws_s3['AWS_ACCESS_KEY']
    AWS_SECRET_KEY = aws_s3['AWS_SECRET_KEY']
    BUCKET_NAME = aws_s3['BUCKET_NAME']
    REGION_NAME = 'ap-northeast-2'

    JWT_SECRET_KEY = keys['JWT_SECRET_KEY']
    JWT_EXPIRATION_DELTA = datetime.timedelta(days=1)
    SESSION_LIFETIME = datetime.timedelta(days=1)

    LIMIT_LEN = 16
    LIMIT = 5

    READCOUNT = 4
    STAR = 6
    MODIFIED_DATE = 5
    TAGS = {'즐길거리': 'fun_m', '쾌적/편리': 'comfort_m', '함께': 'together', '자연/힐링': 'nature_m', '액티비티': 'activity_m',
            '생태교육': 'ecological_s', '둘레길': 'trail_s', '축제': 'festival_s', '문화유적': 'cultural_s',
            '온수잘나오는': 'hot_water_s', '깨끗한': 'clean_s', '차대기편한': 'parking_s', '사이트간격이넓은': 'spacious_s',
            '아이들놀기좋은': 'with_child_s', '가족': 'with_family_s', '커플': 'with_couple_s', '반려견': 'with_pet_s',
            '계곡옆': 'valley_s', '물맑은': 'pure_water_s', '별보기좋은': 'star_s', '힐링': 'healing_s',
            '물놀이하기좋은': 'waterplay_s', '자전거타기좋은': 'bicycle_s', '수영장있는': 'pool_s', '익스트림': 'extreme_s'}
    APPKEY = keys['APPKEY']
    DATE_RANGE = 10

    # 모델링 관련 경로 및 파일 불러오기
    PATH = os.path.abspath('../datas')

    ALGO_POINTS = PATH + '/algo_df_scale.csv'
    ALGO_DF = pd.read_csv(PATH + '/algo_merge_result.csv', encoding="utf-8-sig")
    TAG_DF = pd.read_csv(PATH + '/tag_prior.csv')

    # "weights & tag" dimension 파일 불러오기
    DIMENSION = pd.read_excel(PATH + '/dimension_regression.xlsx')
    DIMENSION = DIMENSION.loc[:, ~DIMENSION.columns.str.contains('^Unnamed')]
    TAG_DM = DIMENSION[['category', 'colname', 'tagname', 'count']].copy()
    TAG_DM.dropna(axis=0, inplace=True)

    RANDOM_RANGE = 10000000

    CLIENT_ID = kakao['CLIENT_ID']
    BASE_URL = 'http://127.0.0.1:5000'
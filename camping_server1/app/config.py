import configparser
import os

config = configparser.ConfigParser()
abspath = os.path.abspath('data.ini')
config.read(abspath)
keys = config['SECRET_KEYS']

class Config(object):
    TEMPLATE_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:' + keys['USER'] + '@' + keys['HOST'] + ':3306/' + keys['DB'] + '?charset=utf8'
    LIMIT = 50
    TAGS = {'즐길거리': 'fun_m', '쾌적/편리': 'comfort_m', '함께': 'together', '자연/힐링': 'nature_m', '액티비티': 'activity_m',
            '생태교육': 'ecological_s', '둘레길': 'trail_s', '축제': 'festival_s', '문화유적': 'cultural_s',
            '온수잘나오는': 'hot_water_s', '깨끗한': 'clean_s', '차대기편한': 'parking_s', '사이트간격이넓은': 'spacious_s',
            '아이들놀기좋은': 'with_child_s', '가족': 'with_family_s', '커플': 'with_couple_s', '반려견': 'with_pet_s',
            '계곡옆': 'valley_s', '물맑은': 'pure_water_s', '별보기좋은': 'star_s', '힐링': 'healing_s',
            '물놀이하기좋은': 'waterplay_s', '자전거타기좋은': 'bicycle_s', '수영장있는': 'pool_s', '익스트림': 'extreme_s'}
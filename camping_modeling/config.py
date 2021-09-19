import configparser
import os
import pandas as pd

config = configparser.RawConfigParser()
abspath = os.path.abspath('../keys/keys.ini')
config.read(abspath)
print("config path: ", abspath)
keys = config['API_KEYS']


class Config:
    PATH = os.path.abspath("../../datas")+"/"
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
               '부산': '부산광역시', '울산': '울산광역시', '대전': '대전광역시', '세종': '세종특별자치시',
               '대구': '대구광역시', '광주': '광주광역시',
               '서울': '서울특별시', '서울시': '서울특별시',
               '제주': '제주특별자치도', '제주도': '제주특별자치도'}

    # 소분류 대분류 카테고리
    CATEGORY = {'재미있는' : '즐길거리',
            '온수 잘 나오는' : '쾌적/편리',
            '아이들 놀기 좋은' : '함께',
            '생태교육' : '즐길거리',
            '가족' : '함께',
            '친절한' : '쾌적/편리',
            '여유있는' : '자연/힐링',
            '깨끗한' : '쾌적/편리',
            '계곡 옆' : '자연/힐링',
            '물놀이 하기 좋은' : '액티비티',
            '물맑은' : '자연/힐링',
            '둘레길' : '즐길거리',
            '별보기 좋은' : '자연/힐링',
            '힐링' : '자연/힐링',
            '커플' : '함께',
            '차 대기 편한' : '쾌적/편리',
            '사이트 간격이 넓은' : '쾌적/편리',
            '축제' : '즐길거리',
            '문화유적' : '즐길거리',
            '자전거 타기 좋은' : '액티비티',
            '그늘이 많은' : '자연/힐링',
            '수영장 있는' : '액티비티',
            '바다가 보이는' : '자연/힐링',
            '익스트림' : '액티비티',
            '반려견' : '함께'}

    CAMP = pd.read_csv(PATH + "camp_api_info_210619.csv", index_col=0)
    FESTIVAL = pd.read_csv(PATH + "festival_210613.csv", index_col=0)
    TOUR = pd.read_csv(PATH + "tour_list_210612.csv", index_col=0)
    CAMP_DETAILS = pd.read_csv(PATH + "crawling_data.csv", encoding='utf-8-sig')

    NAVER = pd.read_csv(PATH + 'v5_category_re.csv')
    KAKAO = pd.read_csv(PATH + 'kakao_camping_review_revised.csv')

    # PAST = pd.read_csv(PATH + 'locgo_visitor_api_info.csv')
    # FUTURE = pd.read_csv(PATH + 'tour_estiDeco_api_info.csv')

    WEIGHTS = pd.read_csv(PATH + 'dimension_weights_sum.csv', index_col=0)
    MAIN_CAT = pd.read_csv(PATH + 'algo_df_max.csv', index_col=0)
    SIGUNGU = pd.read_csv(PATH + 'sigungucode.csv')
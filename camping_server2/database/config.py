import pandas as pd

class Config:
    PATH = "../datas/"
    CAMP = pd.read_csv(PATH + "camp_api_info_210613.csv", index_col=0)
    FESTIVAL = pd.read_csv(PATH + "festival_210613.csv", index_col=0)
    TOUR = pd.read_csv(PATH + "tour_list_210612.csv", index_col=0)
    CAMP_DETAILS = pd.read_csv(PATH + "camp_crawl_links.csv", encoding='utf-8-sig')
        
    NAVER = pd.read_csv(PATH + 'v5_category_re.csv')
    KAKAO = pd.read_csv(PATH + 'kakao_camping_review_revised.csv')

    PAST = pd.read_csv(PATH + 'locgo_visitor_api_info.csv')
    FUTURE = pd.read_csv(PATH + 'tour_estiDeco_api_info.csv')

    WEIGHTS = pd.read_excel(PATH + 'dimension_regression.xlsx')
    MAIN_CAT = pd.read_csv(PATH + 'algo_df_max.csv',index_col=0)
    SIGUNGU = pd.read_csv(PATH + 'sigungucode.csv')

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
 
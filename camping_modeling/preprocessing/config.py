import pandas as pd
from datetime import datetime


class Config:
    # 경로 및 파일 불러오기
    PATH = "../../datas/"
    API_DATA = pd.read_csv(PATH + "camp_api_info_210619.csv", encoding="utf-8-sig")
    CRAWL_DATA = pd.read_csv(PATH + "camp_crawl_links.csv", encoding='utf-8-sig')
    KAKAO = pd.read_csv(PATH + "kk_cat_predict_0805_181611.csv", encoding='utf-8-sig')

    NV_DATA = pd.read_csv(PATH + "v5_category_re.csv", encoding='utf-8-sig')
    KK_DATA = pd.read_csv(PATH + "kakao_camping_review_revised.csv", encoding='utf-8-sig')


    # 파일 버전 저장용 datetime
    TODAY = datetime.today().strftime('%m%d')
    NOW = datetime.today().strftime('%m%d_%H%M%S')
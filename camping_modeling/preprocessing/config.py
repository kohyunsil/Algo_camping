import pandas as pd
from datetime import datetime


class Config:
    # 경로 및 파일 불러오기
    PATH = "../../datas/"
    NV_DATA = pd.read_csv(PATH + "v5_category_re.csv", encoding='utf-8-sig')
    KK_DATA = pd.read_csv(PATH + "kakao_camping_review_revised.csv", encoding='utf-8-sig')


    # 파일 버전 저장용 datetime
    TODAY = datetime.today().strftime('%m%d')
    NOW = datetime.today().strftime('%m%d_%H%M%S')
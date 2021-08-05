import pandas as pd
from datetime import datetime


class Config:
    # 경로 및 파일 불러오기
    PATH = "../../datas/"
    API_DATA = pd.read_csv(PATH + "camp_api_info_210619.csv", encoding="utf-8-sig")
    CRAWL_DATA = pd.read_csv(PATH + "camp_crawl_links.csv", encoding='utf-8-sig')
    NV_DATA = pd.read_csv(PATH + "v5_category_re.csv", encoding='utf-8-sig')
    KK_DATA = pd.read_csv(PATH + "kakao_camping_review_revised.csv", encoding='utf-8-sig')
    ALGO_DF = pd.read_csv(PATH + "algo_df_0719.csv", encoding='utf-8-sig', index_col=0)
    ALGO_DF = ALGO_DF.loc[:, ~ALGO_DF.columns.str.contains('^Unnamed')]
    # ALGO_SCALE = pd.read_csv(PATH + "algo_df_scale.csv", encoding='utf-8-sig', index_col=0)
    # 파일 버전 저장용 datetime
    TODAY = datetime.today().strftime('%m%d')
    NOW = datetime.today().strftime('%m%d_%H%M%S')
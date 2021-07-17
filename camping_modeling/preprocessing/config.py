import pandas as pd


class Config:
    # 경로 및 파일 불러오기
    PATH = "../datas/"
    API_DATA = pd.read_csv(PATH + "camp_api_info_210619.csv", encoding="utf-8-sig")
    CRAWL_DATA = pd.read_csv(PATH + "camp_crawl_links.csv", encoding='utf-8-sig')
    NV_DATA = pd.read_csv(PATH + "v5_category_re.csv", encoding='utf-8-sig')
    KK_DATA = pd.read_csv(PATH + "kakao_review_cat_revised.csv", encoding='utf-8-sig')
    ALGO_SCALE = pd.read_csv(PATH + "algo_df_scale.csv", encoding='utf-8-sig', index_col=0)
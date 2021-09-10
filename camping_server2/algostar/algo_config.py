import pandas as pd
from datetime import datetime
import configparser
import os

config = configparser.RawConfigParser()
abspath = os.path.abspath('../keys/keys.ini')
config.read(abspath)
print("algo_config path: ", abspath)
keys = config['API_KEYS']


class Config:
    # 경로 및 파일 불러오기
    PATH = "../../datas/"
    MODEL_PATH = "../models"
    PUBLIC_API_KEY = keys['PUBLIC_API_KEY']

    # tag_points.py 의 TagMerge를 위한 파일
    API_DATA = pd.read_csv(PATH + "camp_api_info_210619.csv", encoding = "utf-8-sig")
    CRAWL_DATA = pd.read_csv(PATH + "crawling_data.csv", encoding='utf-8-sig')
    ALGO_DF_FINAL = pd.read_csv(PATH + "algo_df_0719.csv", encoding='utf-8-sig', index_col=0)
    ALGO_DF_FINAL = ALGO_DF_FINAL.loc[:, ~ALGO_DF_FINAL.columns.str.contains('^Unnamed')]

    ALGO_DF = pd.read_csv(PATH + "algo_merge_result.csv", encoding="utf-8-sig")
    # "weights & tag" dimension 파일 불러오기
    DIMENSION = pd.read_csv(PATH + "dimension_weights_sum.csv")
    DIMENSION = DIMENSION.loc[:, ~DIMENSION.columns.str.contains('^Unnamed')]
    WEIGHTS_DF = DIMENSION[['category', 'colname', 'weights']].copy()
    WEIGHTS_DF.dropna(axis=0, inplace=True)
    TAG_DM = DIMENSION[['category', 'colname', 'tagname', 'count']].copy()
    TAG_DM.dropna(axis=0, inplace=True)
    # 파일 버전 저장용 datetime
    TODAY = datetime.today().strftime('%m%d')
    NOW = datetime.today().strftime('%m%d_%H%M%S')

    # weights 계산파일
    NV_DATA = pd.read_csv(PATH + "v5_category_re.csv", encoding='utf-8-sig')
    KAKAO = pd.read_csv(PATH + "kk_cat_predict_0805_181611.csv", encoding='utf-8-sig')
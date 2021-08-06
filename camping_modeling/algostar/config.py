import os
import pickle
import pandas as pd
import configparser
from datetime import datetime

config = configparser.RawConfigParser()
abspath = os.path.abspath('../keys/data.ini')
config.read(abspath)
keys = config['API_KEYS']


class Config:
    # 경로 및 파일 불러오기
    PATH = "../../datas/"
    MODEL_PATH = "../models"
    PUBLIC_API_KEY = keys['PUBLIC_API_KEY']
    ALGO_DF = pd.read_csv(PATH + "algo_merge_result.csv", encoding="utf-8-sig")
    TAG_DF = pd.read_csv(PATH + "tag_prior_0720.csv", encoding="utf-8-sig")
    # "weights & tag" dimension 파일 불러오기
    DIMENSION = pd.read_excel(PATH + "dimension_weights_sum.xlsx")
    DIMENSION = DIMENSION.loc[:, ~DIMENSION.columns.str.contains('^Unnamed')]
    WEIGHTS_DF = DIMENSION[['category', 'colname', 'weights']].copy()
    WEIGHTS_DF.dropna(axis=0, inplace=True)
    TAG_DM = DIMENSION[['category', 'colname', 'tagname', 'count']].copy()
    TAG_DM.dropna(axis=0, inplace=True)
    # 파일 버전 저장용 datetime
    TODAY = datetime.today().strftime('%m%d')
    NOW = datetime.today().strftime('%m%d_%H%M%S')

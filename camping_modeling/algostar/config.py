import pandas as pd
import pickle

class Config:
    # 경로 및 파일 불러오기
    PATH = "../../datas/"
    WEIGHTS_DF = pd.read_excel(PATH + "cat_weights.xlsx")
    ALGO_DF = pd.read_csv(PATH+"algo_merge_result.csv", encoding="utf-8-sig")
    with open(PATH + 'weight_dict.txt', 'rb') as wd:
        wd = pickle.load(wd)
        WEIGHTS_DF = pd.DataFrame(wd)
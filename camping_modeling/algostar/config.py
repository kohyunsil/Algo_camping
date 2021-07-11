import pandas as pd
import pickle

class Config:
    # 경로 및 파일 불러오기
    PATH = "../../datas/"
    ALGO_DF = pd.read_csv(PATH+"algo_merge_result.csv", encoding="utf-8-sig")
    WEIGHTS = pd.read_excel(PATH + "cat_weights2.xlsx")
    wdf = WEIGHTS[['category', 'colname', 'weights']]
    weight_dict = wdf.to_dict('records')
    with open(PATH + 'weight_dict.txt', 'wb') as wd:
        pickle.dump(weight_dict, wd)
    with open(PATH + 'weight_dict.txt', 'rb') as wd:
        wd = pickle.load(wd)
        WEIGHTS_DF = pd.DataFrame(wd)
    KAKAO = pd.read_csv(PATH+'kakao_review_cat_revised.csv')
    NAVER = pd.read_csv(PATH+'v5_category_re.csv')

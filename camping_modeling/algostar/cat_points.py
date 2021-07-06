import pandas as pd
import numpy as np

class Calc_logic:
    def __init__(self):
        pass
    def binary_calc(self, data, colname, con1, h_point, l_point):
        """값의 유무에 따라 0 또는 1점 부여하는 이진 점수화
        h_point에 높은 점수, l_point에 낮은 점수 기입"""
        target_df = pd.DataFrame(data[f'{colname}'].isnull() == True)
        target_df[f'{colname}'] = [l_point if r == True else h_point for r in target_df[f'{colname}']]
        target_df

    def cls_calc(self, data, colname, c1, c2, c3, p1, p2, p3):
        """3개의 분류로 점수 부여
        condition(c1, c2, c3) type이 string / int 인지 파악 후 조건 함수 작성"""
        pass

    def percent_calc(self, data, colname):
        """percentile 기준 백분율 점수"""



class Cat5_points:
    def __init__(self):
        self.path = "../../datas/"
        self.camp_df = pd.read_csv(self.path+"camp_data_merge.csv", encoding="utf-8-sig")
        self.review_df = pd.read_csv(self.path+"review_final_point.csv", encoding="utf-8-sig")
        self.weights = pd.read_csv(self.path+"cat_weights.csv", encoding="utf-8-sig")

    def comfort_point(self):
        comfort_df = camp_df[['insrncAt','trsagntNo','mangeDivNm','manageNmpr','sitedStnc','glampInnerFclty',
                              'caravInnerFclty','trlerAcmpnyAt','caravAcmpnyAt','trlerAcmpnyAt','caravAcmpnyAt',
                              'toiletCo','swrmCo','wtrplCo','brazierCl','sbrsCl','sbrsEtc','posblFcltyCl',
                              'extshrCo','frprvtWrppCo','frprvtSandCo','fireSensorCo']].copy()

    def together_point(self):
        pass
    def fun_point(self):
        pass
    def healing_point(self):
        pass
    def clean_point(self):
        pass

import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore", UserWarning)


class Calc_logic:
    def __init__(self):
        pass

    def binary_calc(self, data, colname, h_point, l_point, h_con):
        """
        특정 조건에 따라 True/False 이진 점수화
        h_point에 높은 점수, l_point에 낮은 점수 기입, h_point 를 받는 조건을 h_con 에 기입
        (1) h_con = int/float (ex: 3 이상 : 1점 / 3 미만 : 0점)
        (2) h_con = 'notnull' (ex: 번호 있으면 1점 / 없으면 0점)
        (3) h_con = f'{string}' (ex: 직영 1점 / 위탁 0점 -> string='직영')
        """
        if type(h_con) != str:
            target_df = pd.DataFrame(data[f'{colname}'] >= h_con)
        elif h_con == 'notnull':
            target_df = pd.DataFrame(data[f'{colname}'].isnull() == False)
        else:
            target_df = pd.DataFrame(data[f'{colname}'] == h_con)
        target_df[f'{colname}'] = [h_point if r == True else l_point for r in target_df[f'{colname}']]
        return target_df

    def cls_calc(self, data, colname, c1, c2, c3, p1, p2, p3):
        """
        3개의 분류로 점수 부여
        condition(c1, c2, c3) type이 string / int 인지 파악 후 조건 함수 작성
        manageNmpr  int     / 3명(c1) 이상: 10점(p1)/ 2명이하(c2): 5점(p2)/ 0은(c3) 0점(p3)
        brazierCl   str     / 개별(c1) 2점(p1) / 공동취사장(c2) 1점(p2)/ 불가(c3) 0점(p3)
        """

        if type(c1) != str:
            def func(x):
                if x >= c1:
                    return p1
                elif c3 < x <= c2:
                    return p2
                else:
                    return p3
            target_df = pd.DataFrame(data[f'{colname}'])
            target_df[f'{colname}'] = target_df[f'{colname}'].apply(lambda x: func(x))

        else:
            def func(x):
                if x == c1:
                    return p1
                elif x == c2:
                    return p2
                else:
                    return p3

            target_df = pd.DataFrame(data[f'{colname}'])
            target_df[f'{colname}'] = target_df[f'{colname}'].apply(lambda x: func(x))

        return target_df

    def percent_calc(self, data, colname):
        """percentile 기준 백분율 점수"""
        target_df = pd.DataFrame(data[f'{colname}'])
        target_df[f'{colname}'] = target_df[f'{colname}'].rank(pct=True)
        return target_df


class Calc_weights:
    def __init__(self):
        self.path = "../../datas/"
        self.weights = pd.read_excel(self.path + "cat_weights.xlsx")
        self.df = pd.read_csv(self.path+"algo_merge_result.csv", encoding="utf-8-sig")

    def get_weights(self, category, origindf, colname):
        df = self.weights
        weights = df[df['category']==category][df['origindf']==origindf][df['colname']==colname]['weights']
        return float(weights)

    def get_cat_df(self, category):
        cp_df = self.df[self.get_col_list(category, 'camp').append('camp')]
        rv_df = self.df[self.get_col_list(category, 'review').append('camp')]
        return cp_df, rv_df

    def get_col_list(self, category, origindf=None):
        df = self.weights
        if origindf == None:
            result = df[df['category'] == category]['colname']
        else:
            result = df[df['category']==category][df['origindf']==origindf]['colname']
        return result.tolist()

    def weights_list(self, category, origindf):
        weights_list = [self.get_weights(category, origindf, a) for a in self.get_col_list(category, origindf)]
        return weights_list

class Cat5_points(Calc_logic, Calc_weights):

    def __init__(self):
        super().__init__()
        self.path = "../../datas/"
        self.weights = pd.read_excel(self.path + "cat_weights.xlsx")
        self.df = pd.read_csv(self.path+"algo_merge_result.csv", encoding="utf-8-sig")
        self.camp_df = pd.read_csv(self.path+"camp_algo_merge.csv", encoding="utf-8-sig")
        self.review_df = pd.read_csv(self.path+"review_final_point.csv", encoding="utf-8-sig")


    def comfort_point(self):
        pass

    def together_point(self, campname, category='together'):
        cp_df, rv_df = self.get_cat_df(category)
        rv_col_ls, cp_col_ls = self.get_col_list(category, 'review'), self.get_col_list(category, 'camp')
        result = 0
        print(rv_col_ls)
        for colname in rv_col_ls:
            weight = self.get_weights(category, 'review', colname)
            point = rv_df[rv_df['camp']==campname][rv_df['category']==colname]['final_point']
            point = float(point).round(1)
            result += weight * point
        rv_points = result

        print(rv_points)



    def fun_point(self):
        pass
    def healing_point(self):
        pass
    def clean_point(self):
        pass

if __name__ == '__main__':
    cl = Calc_logic()
    # cl.percent_calc()
    # cls_calc(data, colname, c1, c2, c3, p1, p2, p3)
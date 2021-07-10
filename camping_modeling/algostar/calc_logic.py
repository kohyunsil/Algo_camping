import pandas as pd
import numpy as np
import config as config


class CalcLogic:
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
        target_df[f'{colname}'] = [h_point if r is True else l_point for r in target_df[f'{colname}']]
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
                elif 0 < x <= c3:
                    return p3
                else:
                    return 0

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
        target_df[f'{colname}'] = target_df[f'{colname}'].rank(method='dense', pct=True)
        return target_df


class CalcWeights:
    def __init__(self):
        self.path = config.Config.PATH
        self.weights = config.Config.WEIGHTS_DF
        self.df = config.Config.ALGO_DF

    def get_weights(self, category, colname):
        df = self.weights
        weights = df[df['category'] == category][df['colname'] == colname]['weights']
        return float(weights)

    def get_cat_df(self, category, origindf):
        self.df.set_index('contentId', drop=False, inplace=True)
        df = self.df[self.get_col_list(category, origindf)]
        return df

    def get_col_list(self, category, origindf=None):
        df = self.weights
        result = df[df['category'] == category]['colname']
        if origindf is None:
            pass
        elif origindf == 'review':
            result = result[[r[-2:] == '_r' for r in result]]
        elif origindf == 'tag':
            result = result[[r[-2:] == '_s' for r in result]]
        elif origindf == 'camp':
            result = result[[(r[-2:] != '_r' and r[-2:] != '_s') for r in result]]
        else:
            print(f"Here's the whole colnames of the '{category}'.")
            print("please enter the right origin_df (review / tag /camp)")
        # print(f"{origindf} column list: ", result.tolist())
        return result.tolist()

    def multiply_weights(self, category, origindf, camp_id):
        self.df.set_index('contentId', drop=False, inplace=True)
        col_ls = self.get_col_list(category, origindf)
        result = 0
        for colname in col_ls:
            weight = self.get_weights(category, colname)
            point = self.df[f'{colname}'].loc[camp_id]
            result += weight * float(point)
        if origindf == "review":
            point = np.round(result / 5, 1)
        else:
            point = np.round(result, 1)
        return point

import pandas as pd
import numpy as np
import warnings

warnings.simplefilter("ignore", UserWarning)
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
                elif x == 0:
                    return 0
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
        # print(f"{category} {origindf} point: ", point)
        return point


class Cat5Points(CalcLogic, CalcWeights):

    def __init__(self):
        super().__init__()
        self.path = config.Config.PATH
        self.weights = config.Config.WEIGHTS_DF
        self.df = config.Config.ALGO_DF

    def comfort_point(self, camp_id, category='comfort'):
        # 1. 리뷰 point /5 * weights
        rv_point = self.multiply_weights(category, 'review', camp_id)
        # 2. 태그 * weights
        tg_point = self.multiply_weights(category, 'tag', camp_id)
        # 3. 캠핑 API * weights
        cp_df = self.get_cat_df(category, 'camp')
        cp_1 = self.binary_calc(cp_df, 'insrncAt', 1, 0, 'Y').loc[camp_id]
        cp_2 = self.binary_calc(cp_df, 'trsagntNo', 1, 0, 'notnull').loc[camp_id]
        cp_3 = self.binary_calc(cp_df, 'mangeDivNm', 1, 0, '직영').loc[camp_id]
        cp_4 = self.binary_calc(cp_df, 'sitedStnc', 1, 0, 3).loc[camp_id]
        cp_5 = self.binary_calc(cp_df, 'trlerAcmpnyAt', 1, 0, 'Y').loc[camp_id]
        cp_6 = self.binary_calc(cp_df, 'caravAcmpnyAt', 1, 0, 'Y').loc[camp_id]
        cp_7 = self.cls_calc(cp_df, 'manageNmpr', 3, 2, 1, 10, 2, 1).loc[camp_id]
        cp_8 = self.cls_calc(cp_df, 'glampInnerFclty', 5, 3, 2, 3, 2, 1).loc[camp_id]
        cp_9 = self.cls_calc(cp_df, 'caravInnerFclty', 5, 3, 2, 3, 2, 1).loc[camp_id]
        cp_10 = self.cls_calc(cp_df, 'brazierCl', '개별', '공동취사장', '불가', 2, 1, 0).loc[camp_id]
        cp_11 = self.cls_calc(cp_df, 'sbrsCl', 5, 3, 2, 10, 5, 1).loc[camp_id]
        cp_12 = self.cls_calc(cp_df, 'sbrsEtc', 5, 3, 2, 5, 3, 2).loc[camp_id]
        cp_13 = self.cls_calc(cp_df, 'posblFcltyCl', 5, 3, 2, 5, 3, 2).loc[camp_id]

        pct_col_list = ['toiletCo', 'swrmCo', 'wtrplCo', 'extshrCo', 'frprvtWrppCo', 'frprvtSandCo', 'fireSensorCo']
        cp_pct = 0
        for colname in pct_col_list:
            p = self.percent_calc(cp_df, colname).loc[camp_id] * self.get_weights(category, colname)
            cp_pct += float(p)

        cp_point = float(cp_1) + float(cp_2) + float(cp_3) + float(cp_4) + float(cp_5) +\
                   float(cp_6) + float(cp_7) + float(cp_8) + float(cp_9) + float(cp_10) +\
                   float(cp_11) + float(cp_12) + float(cp_13) + cp_pct

        points = round(rv_point + tg_point + cp_point, 1)
        # print(f"{camp_id} - {category} point: {points}")
        return points

    def together_point(self, camp_id, category='together'):
        # 1. 리뷰 point /5 * weights
        rv_point = self.multiply_weights(category, 'review', camp_id)
        # 2. 태그 * weights
        tg_point = self.multiply_weights(category, 'tag', camp_id)
        # 3. 캠핑 API * weights
        cp_df = self.get_cat_df(category, 'camp')
        cp_1 = self.cls_calc(cp_df, 'sbrsEtc', 5, 3, 2, 15, 10, 5).loc[camp_id]
        cp_2 = self.cls_calc(cp_df, 'posblFcltyCl', 5, 3, 2, 15, 10, 5).loc[camp_id]
        cp_3 = self.cls_calc(cp_df, 'animalCmgCl', '가능', '가능(소형견)', '불가', 15, 10, 0).loc[camp_id]
        cp_point = float(cp_1) + float(cp_2) + float(cp_3)

        points = rv_point + tg_point + cp_point
        # print(f"{camp_id} - {category} point: {points}")
        return points

    def fun_point(self, camp_id, category='fun'):
        # 1. 리뷰 point /5 * weights
        rv_point = self.multiply_weights(category, 'review', camp_id)
        # 2. 태그 * weights
        tg_point = self.multiply_weights(category, 'tag', camp_id)
        # 3. 캠핑 API * weights
        cp_df = self.get_cat_df(category, 'camp')
        cp_1 = self.cls_calc(cp_df, 'sbrsEtc', 5, 3, 2, 15, 10, 5).loc[camp_id]
        cp_2 = self.cls_calc(cp_df, 'posblFcltyCl', 5, 3, 2, 15, 10, 5).loc[camp_id]
        cp_point = float(cp_1) + float(cp_2)

        points = rv_point + tg_point + cp_point
        # print(f"{camp_id} - {category} point: {points}")
        return points

    def healing_point(self, camp_id, category='healing'):
        # 1. 리뷰 point /5 * weights
        rv_point = self.multiply_weights(category, 'review', camp_id)
        # 2. 태그 * weights
        tg_point = self.multiply_weights(category, 'tag', camp_id)
        # 3. 캠핑 API * weights
        cp_df = self.get_cat_df(category, 'camp')
        cp_1 = self.cls_calc(cp_df, 'brazierCl', '개별', '공동 화로', '불가', 5, 2, 0)
        cp_point = float(cp_1.loc[camp_id])

        points = rv_point + tg_point + cp_point
        return points

    def clean_point(self, camp_id, category='clean'):
        # 1. 리뷰 point /5 * weights
        rv_point = self.multiply_weights(category, 'review', camp_id)
        # 2. 태그 * weights
        tg_point = self.multiply_weights(category, 'tag', camp_id)

        points = rv_point + tg_point
        return points


class AlgoPoints(Cat5Points):

    def __init__(self):
        super().__init__()
        self.path = config.Config.PATH
        self.df = config.Config.ALGO_DF

    def polar_points(self, camp_id):
        comfort_point = self.comfort_point(camp_id)
        together_point = self.together_point(camp_id)
        fun_point = self.fun_point(camp_id)
        healing_point = self.healing_point(camp_id)
        clean_point = self.clean_point(camp_id)
        total_point = comfort_point + together_point + fun_point + healing_point + clean_point
        total_point = round(total_point, 1)

        print(f"{camp_id} - total point: {total_point}점 - comfort: {comfort_point} / together: {together_point} /"
              f"fun: {fun_point} / healing: {healing_point} / clean: {clean_point}")
        return [comfort_point, together_point, fun_point, healing_point, clean_point]

    def algo_star(self, camp_id):
        total_point = sum(self.polar_points(camp_id))
        algo_star = np.round(total_point / 100, 1)
        print(f"{camp_id} - algo star: 별이 {algo_star}개!")
        return algo_star

    def make_alfo_df(self):
        algo_df = self.df[['contentId', 'camp']]
        comfort, together, fun, healing, clean = [], [], [], [], []
        for idx in self.df['contentId'].tolist():
            polar_list = self.polar_points(idx)
            comfort.append(polar_list[0])
            together.append(polar_list[1])
            fun.append(polar_list[2])
            healing.append(polar_list[3])
            clean.append(polar_list[4])
        algo_df['comfort'] = comfort
        algo_df['together'] = together
        algo_df['fun'] = fun
        algo_df['healing'] = healing
        algo_df['clean'] = clean

        algo_df.to_csv(self.path+"algo_df.csv", encoding='utf-8-sig')
        return algo_df



if __name__ == '__main__':
    cl = CalcLogic()
    cw = CalcWeights()
    c5 = Cat5Points()
    ap = AlgoPoints()

    # cw.get_col_list('comfort', 'camp')
    # c5.together_point('답게')
    # c5.healing_point('별똥별 글램핑')

    # ap.polar_points('답게')
    # ap.algo_star(7959)
    ap.make_alfo_df()

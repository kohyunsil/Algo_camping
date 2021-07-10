import pandas as pd
import numpy as np
import warnings
import config as config
import calc_logic as cl
warnings.simplefilter("ignore", UserWarning)


class Cat5Points(cl.CalcLogic, cl.CalcWeights):

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
        cp_1 = self.binary_calc(cp_df, 'insrncAt', self.get_weights(category, 'insrncAt'), 0, 'Y').loc[camp_id]
        cp_2 = self.binary_calc(cp_df, 'trsagntNo', self.get_weights(category, 'trsagntNo'), 0, 'notnull').loc[camp_id]
        cp_3 = self.binary_calc(cp_df, 'mangeDivNm', self.get_weights(category, 'mangeDivNm'), 0, '직영').loc[camp_id]
        cp_4 = self.binary_calc(cp_df, 'trlerAcmpnyAt', self.get_weights(category, 'trlerAcmpnyAt'), 0, 'Y').loc[camp_id]
        cp_5 = self.binary_calc(cp_df, 'caravAcmpnyAt', self.get_weights(category, 'caravAcmpnyAt'), 0, 'Y').loc[camp_id]
        cp_6 = self.cls_calc(cp_df, 'brazierCl', '개별', '공동취사장', '불가',
                             self.get_weights(category, 'brazierCl'), self.get_weights(category, 'brazierCl')/2, 0).loc[camp_id]

        pct_col_list = ['sitedStnc', 'manageNmpr', 'glampInnerFclty', 'caravInnerFclty', 'sbrsCl', 'sbrsEtc', 'posblFcltyCl',
                        'toiletCo', 'swrmCo', 'wtrplCo', 'extshrCo', 'frprvtWrppCo', 'frprvtSandCo', 'fireSensorCo']
        cp_pct = 0
        for colname in pct_col_list:
            p = self.percent_calc(cp_df, colname).loc[camp_id] * self.get_weights(category, colname)
            cp_pct += float(p)

        cp_point = float(cp_1) + float(cp_2) + float(cp_3) + float(cp_4) + float(cp_5) + float(cp_6) + cp_pct

        points = round(rv_point + tg_point + cp_point, 1)
        return points

    def together_point(self, camp_id, category='together'):
        # 1. 리뷰 point /5 * weights
        rv_point = self.multiply_weights(category, 'review', camp_id)
        # 2. 태그 * weights
        tg_point = self.multiply_weights(category, 'tag', camp_id)
        # 3. 캠핑 API * weights
        cp_df = self.get_cat_df(category, 'camp')
        cp_1 = self.cls_calc(cp_df, 'animalCmgCl', '가능', '가능(소형견)', '불가',
                             self.get_weights(category, 'animalCmgCl'), self.get_weights(category, 'animalCmgCl')/2, 0).loc[camp_id]

        pct_col_list = ['sbrsEtc', 'posblFcltyCl']
        cp_pct = 0
        for colname in pct_col_list:
            p = self.percent_calc(cp_df, colname).loc[camp_id] * self.get_weights(category, colname)
            cp_pct += float(p)
        cp_point = float(cp_1) + cp_pct

        points = round(rv_point + tg_point + cp_point, 1)
        return points

    def fun_point(self, camp_id, category='fun'):
        # 1. 리뷰 point /5 * weights
        rv_point = self.multiply_weights(category, 'review', camp_id)
        # 2. 태그 * weights
        tg_point = self.multiply_weights(category, 'tag', camp_id)
        # 3. 캠핑 API * weights
        cp_df = self.get_cat_df(category, 'camp')
        pct_col_list = ['sbrsEtc', 'posblFcltyCl']
        cp_pct = 0
        for colname in pct_col_list:
            p = self.percent_calc(cp_df, colname).loc[camp_id] * self.get_weights(category, colname)
            cp_pct += float(p)
        cp_point = cp_pct

        points = round(rv_point + tg_point + cp_point, 1)
        return points

    def healing_point(self, camp_id, category='healing'):
        # 1. 리뷰 point /5 * weights
        rv_point = self.multiply_weights(category, 'review', camp_id)
        # 2. 태그 * weights
        tg_point = self.multiply_weights(category, 'tag', camp_id)
        # 3. 캠핑 API * weights
        cp_df = self.get_cat_df(category, 'camp')
        cp_1 = self.cls_calc(cp_df, 'brazierCl', '개별', '공동취사장', '불가',
                             self.get_weights(category, 'brazierCl'), self.get_weights(category, 'brazierCl')/2, 0).loc[camp_id]
        cp_point = float(cp_1)

        points = round(rv_point + tg_point + cp_point, 1)
        return points

    def clean_point(self, camp_id, category='clean'):
        # 1. 리뷰 point /5 * weights
        rv_point = self.multiply_weights(category, 'review', camp_id)
        # 2. 태그 * weights
        tg_point = self.multiply_weights(category, 'tag', camp_id)

        points = rv_point + tg_point
        return points

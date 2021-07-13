import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
import app.config as config
import app.service.catpoints as cp

warnings.simplefilter("ignore")


class AlgoPoints(cp.Cat5Points):
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

        return [comfort_point, together_point, fun_point, healing_point, clean_point]

    def algo_star(self, camp_id):
        total_point = sum(self.polar_points(camp_id))
        polar_score = self.polar_points(camp_id)

        algo_star = np.round(total_point / 100, 1)
        return algo_star, polar_score

    def make_algo_df(self, just_load_file=True):
        """default: 저장되어있는 파일을 불러온다.
        새로 점수 산출을 하려면 just_load_file=False로 설정"""

        if just_load_file:
            # 불러올 저장된 파일명을 기입해주세요.
            algo_df = pd.read_csv(self.path + f"algo_df_0713.csv", encoding='utf-8-sig')

        else:
            algo_df = self.df[['contentId', 'camp']]
            comfort, together, fun, healing, clean = [], [], [], [], []
            for idx in tqdm(algo_df['contentId'].tolist()):
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

        return algo_df

import pandas as pd
import numpy as np
from itertools import product
import math


class UserPoints:
    def __init__(self):
        self.survey_weight = [5, 10, 10, 15, 10, 20, 20, 10]

    def a100_answer(self, answer):
        survey_weight = self.survey_weight[0]
        comfort_ls = [2, 2, 2, 3, 5]
        clean_ls = [2, 2, 2, 3, 5]
        comfort_point = comfort_ls[answer-1] * survey_weight
        clean_point = clean_ls[answer - 1] * survey_weight
        return [comfort_point, 0, 0, 0, clean_point]

    def a200_answer(self, answer):
        survey_weight = self.survey_weight[1]
        together_ls = [5, 3, 3, 0]
        together_point = together_ls[answer-1] * survey_weight
        return [0, together_point, 0, 0, 0]

    def a210_answer(self, answer):
        survey_weight = self.survey_weight[2]
        together_ls = [5, 0]
        together_point = together_ls[answer-1] * survey_weight
        return [0, together_point, 0, 0, 0]

    def a300_answer(self, answer):
        survey_weight = self.survey_weight[3]
        comfort_ls = [5, 10, 0]
        fun_ls = [3, 1, 5]
        clean_ls = [5, 10, 0]
        comfort_point = comfort_ls[answer-1] * survey_weight
        fun_point = fun_ls[answer - 1] * survey_weight
        clean_point = clean_ls[answer - 1] * survey_weight
        return [comfort_point, 0, fun_point, 0, clean_point]

    def a410_answer(self, answer):
        survey_weight = self.survey_weight[4]
        together_ls = [3, 5, 3, 3]
        fun_ls = [5, 10, 5, 3]
        together_point = together_ls[answer-1] * survey_weight
        fun_point = fun_ls[answer - 1] * survey_weight
        return [0, together_point, fun_point, 0, 0]

    def a420_answer(self, answer):
        survey_weight = self.survey_weight[5]
        comfort_ls = [2, 2, 2, 5]
        fun_ls = [5, 5, 1, 1]
        healing_ls = [5, 5, 5, 2]
        clean_ls = [2, 2, 2, 5]
        comfort_point = comfort_ls[answer - 1] * survey_weight
        fun_point = fun_ls[answer - 1] * survey_weight
        healing_point = healing_ls[answer - 1] * survey_weight
        clean_point = clean_ls[answer - 1] * survey_weight
        return [comfort_point, 0, fun_point, healing_point, clean_point]

    def a500_answer(self, answer):
        survey_weight = self.survey_weight[6]
        together_ls = [5, 1, 3, 3]
        fun_ls = [5, 1, 3, 2]
        healing_ls = [2, 5, 3, 1]
        together_point = together_ls[answer - 1] * survey_weight
        fun_point = fun_ls[answer - 1] * survey_weight
        healing_point = healing_ls[answer - 1] * survey_weight
        return [0, together_point, fun_point, healing_point, 0]

    def a600_answer(self, answer):
        survey_weight = self.survey_weight[7]
        comfort_ls = [5, 1, 1, 1, 1, 1]
        fun_ls = [1, 5, 5, 5, 5, 5]
        healing_ls = [1, 5, 5, 5, 5, 5]
        comfort_point = comfort_ls[answer - 1] * survey_weight
        fun_point = fun_ls[answer - 1] * survey_weight
        healing_point = healing_ls[answer - 1] * survey_weight
        return [comfort_point, 0, fun_point, healing_point, 0]

    def calc_cat_point(self, answer_ls):
        ls100 = self.a100_answer(answer_ls[0])
        ls200 = self.a200_answer(answer_ls[1])
        ls210 = self.a210_answer(answer_ls[2])
        ls300 = self.a300_answer(answer_ls[3])
        ls410 = self.a410_answer(answer_ls[4])
        ls420 = self.a420_answer(answer_ls[5])
        ls500 = self.a500_answer(answer_ls[6])
        ls600 = self.a600_answer(answer_ls[7])
        result_ls = [ls100[i] + ls200[i] + ls210[i] + ls300[i] + ls410[i] + ls420[i] + ls500[i] + ls600[i] for i in range(len(ls100))]
        return result_ls

    def calc_final_point(self, user_answer_ls):
        result_ls = self.calc_cat_point(user_answer_ls)
        questions = [[i for i in range(1, 6)],
                     [i for i in range(1, 5)],
                     [i for i in range(1, 3)],
                     [i for i in range(1, 4)],
                     [i for i in range(1, 5)],
                     [i for i in range(1, 5)],
                     [i for i in range(1, 5)],
                     [i for i in range(1, 7)]]
        answer_ls = list(product(*questions))
        comfort_ls, together_ls, fun_ls, healing_ls, clean_ls = [], [], [], [], []
        for answer in answer_ls:
            result = self.calc_cat_point(answer)
            comfort_ls.append(result[0])
            together_ls.append(result[1])
            fun_ls.append(result[2])
            healing_ls.append(result[3])
            clean_ls.append(result[4])

        comfort_point = result_ls[0] / max(comfort_ls)*100
        together_point = result_ls[1] / max(together_ls)*100
        fun_point = result_ls[2] / max(fun_ls)*100
        healing_point = result_ls[3] / max(healing_ls)*100
        clean_point = result_ls[4] / max(clean_ls)*100

        return [comfort_point, together_point, fun_point, healing_point, clean_point]


class PolarArea(UserPoints):
    def __init__(self):
        super().__init__()

    def calc_polar_area(self, result_ls):
        # result_ls = self.calc_cat_point(answer_ls)
        comfort_together = result_ls[0] * result_ls[1] * math.sin(360/5) / 2
        together_fun = result_ls[1] * result_ls[2] * math.sin(360 / 5) / 2
        fun_healing = result_ls[2] * result_ls[3] * math.sin(360 / 5) / 2
        healing_clean = result_ls[3] * result_ls[4] * math.sin(360 / 5) / 2
        clean_comfort = result_ls[4] * result_ls[0] * math.sin(360 / 5) / 2
        area = comfort_together + together_fun + fun_healing + healing_clean + clean_comfort
        return area

    def matching_pct(self, camp_point_ls, user_point_ls):
        pct_ls = []
        for i in range(len(camp_point_ls)):

            pct = camp_point_ls[i] / user_point_ls[i]
            if pct >= 1:
                pct_ls.append(1/pct)
            elif pct == 0:
                pass
            else:
                pct_ls.append(pct)
        return np.round(np.average(pct_ls) * 100, 1)
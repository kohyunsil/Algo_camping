import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))
import pandas as pd
import numpy as np
import random
import math
from itertools import product
import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
import recommend_df as rd
import recommend_copywrite as cw
import camping_server2.db.sql_create as sc
import camping_server2.algostar.user_points as up
rec = rd.UserWeights()
write = cw.CopyWriting()
sql = sc.Query()
polar = up.PolarArea()


class UserAnswer:
    def __init__(self):
        self.IP = sql.IP
        self.DB = sql.DB
        self.PW = sql.PW

    def read_db(self, id):
        """DB.user 테이블에서 유저가 등록한 응답 불러오기"""
        cursor, engine, db = sql.connect_sql()
        query = f"select * from user where id = {id}"
        cursor.execute(query)
        result = cursor.fetchall()
        result_df = pd.DataFrame(result)
        result_df = result_df[['id', 'A100', 'A200', 'A210', 'A300', 'A410', 'A420', 'A500', 'A600']].copy()
        result_df.set_index('id', drop=True, inplace=True)
        return result_df

    def get_answer_ls(self, id):
        result_df = self.read_db(id)
        answer_ls = result_df.loc[id].tolist()
        answer_ls = [int(ans) for ans in answer_ls]
        return answer_ls


class Scenario:
    def __init__(self):
        pass

    def main_a200(self, answer, row=20):
        copy = write.copy_a200(answer)
        df = rec.reco_a200()[answer][['contentId', 'facltNm', 'firstImageUrl']][:row]
        return copy, df

    def main_a210(self, answer, row=20):
        copy = write.copy_a210(answer)
        df = rec.reco_a210()[answer][['contentId', 'facltNm', 'firstImageUrl']][:row]
        return copy, df

    def main_a300(self, answer, row=20):
        copy = write.copy_a300(answer)
        df = rec.reco_a300()[answer][['contentId', 'facltNm', 'firstImageUrl']][:row]
        return copy, df

    def main_a410(self, answer, row=20):
        season, copy = write.copy_a410(answer, now=True)
        df = rec.reco_a410()[season][['contentId', 'facltNm', 'firstImageUrl']][:row]
        return copy, df

    def main_a420(self, answer, row=20):
        copy = write.copy_a420(answer)
        df = rec.reco_a420()[answer][['contentId', 'facltNm', 'firstImageUrl']][:row]
        return copy, df

    def main_a500(self, answer, row=20):
        copy = write.copy_a500(answer)
        df = rec.reco_a500()[answer][['contentId', 'facltNm', 'firstImageUrl']][:row]
        return copy, df

    def main_a600(self, answer, row=20):
        copy = write.copy_a600(answer)
        df = rec.reco_a600()[answer][['contentId', 'facltNm', 'firstImageUrl']][:row]
        return copy, df


if __name__ == '__main__':
    user = UserAnswer()
    # result_df = user.read_db(63)
    # print(result_df)
    # answer_ls = user.get_answer_ls(63)
    # print(answer_ls)
    # print("user polar points: ", polar.calc_final_point(answer_ls))

    scene = Scenario()
    # 설문 응답 경우의 수 list
    questions = [[i for i in range(1, 5)],  #a200
                 [i for i in range(1, 3)],  #a210
                 [i for i in range(1, 4)],  #a300
                 [i for i in range(1, 5)],  #a410
                 [i for i in range(1, 5)],  #a420
                 [i for i in range(1, 5)],  #a500
                 [i for i in range(1, 7)]]  #a600
    answer_ls = random.choice(list(product(*questions)))

    copy200, df200 = scene.main_a200(answer_ls[0])
    copy210, df210 = scene.main_a210(answer_ls[1])
    copy300, df300 = scene.main_a300(answer_ls[2])
    copy410, df410 = scene.main_a410(answer_ls[3])
    copy420, df420 = scene.main_a420(answer_ls[4])
    copy500, df500 = scene.main_a500(answer_ls[5])
    copy600, df600 = scene.main_a600(answer_ls[6])

    print(copy500)
    print(df500.columns)
    print(df500)

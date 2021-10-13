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


class AccessDb:
    def __init__(self):
        self.IP = sql.IP
        self.DB = sql.DB
        self.PW = sql.PW

    def read_user_db(self, id):
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
        result_df = self.read_user_db(id)
        answer_ls = result_df.loc[id].tolist()
        answer_ls = [int(ans) for ans in answer_ls]
        return answer_ls

    def read_algopoint_db(self):
        cursor, engine, db = sql.connect_sql()
        query = f"select * from algopoint"
        cursor.execute(query)
        result = cursor.fetchall()
        result_df = pd.DataFrame(result)
        result_df.set_index('content_id', drop=True, inplace=True)
        result_df = pd.DataFrame(index=result_df.index, data=result_df.sum(axis=1), columns=['algopoint'])
        result_df.reset_index(inplace=True)
        result_df.rename(columns={'content_id': 'contentId'}, inplace=True)
        print(result_df.columns)
        return result_df

    def mix_merge(self, merge_df, row=None):
        merge_df.rename(columns={'facltNm_y': 'facltNm', 'firstImageUrl_y': 'firstImageUrl',
                                   'algopoint_y': 'algopoint'}, inplace=True)
        merge_df.dropna(subset=['firstImageUrl'], inplace=True)
        df = merge_df[['contentId', 'facltNm', 'firstImageUrl']][:row]
        return df


class Scenario(AccessDb):
    def __init__(self):
        super().__init__()
        self.algopoint = self.read_algopoint_db()

    def main_a200(self, answer, row=None):
        copy = write.copy_a200(answer)
        df = rec.reco_a200()[answer][['contentId', 'facltNm', 'firstImageUrl']]
        df = pd.merge(df, self.algopoint, how='left', on='contentId')
        df = df.sort_values('algopoint', ascending=False)[:row]
        return [copy, df]

    def main_a210(self, answer, row=None):
        copy = write.copy_a210(answer)
        df = rec.reco_a210()[answer][['contentId', 'facltNm', 'firstImageUrl']]
        df = pd.merge(df, self.algopoint, how='left', on='contentId')
        df = df.sort_values('algopoint', ascending=False)[:row]
        return [copy, df]

    def main_a300(self, answer, row=None):
        copy = write.copy_a300(answer)
        df = rec.reco_a300()[answer][['contentId', 'facltNm', 'firstImageUrl']]
        df = pd.merge(df, self.algopoint, how='left', on='contentId')
        df = df.sort_values('algopoint', ascending=False)[:row]
        return [copy, df]

    def main_a410(self, answer, row=None):
        season, copy = write.copy_a410(answer, now=True)
        df = rec.reco_a410()[season][['contentId', 'facltNm', 'firstImageUrl']]
        df = pd.merge(df, self.algopoint, how='left', on='contentId')
        df = df.sort_values('algopoint', ascending=False)[:row]
        return [copy, df]

    def main_a420(self, answer, row=None):
        copy = write.copy_a420(answer)
        df = rec.reco_a420()[answer][['contentId', 'facltNm', 'firstImageUrl']]
        df = pd.merge(df, self.algopoint, how='left', on='contentId')
        df = df.sort_values('algopoint', ascending=False)[:row]
        return [copy, df]

    def main_a500(self, answer, row=None):
        copy = write.copy_a500(answer)
        df = rec.reco_a500()[answer][['contentId', 'facltNm', 'firstImageUrl']]
        df = pd.merge(df, self.algopoint, how='left', on='contentId')
        df = df.sort_values('algopoint', ascending=False)[:row]
        return [copy, df]

    def main_a600(self, answer, row=None):
        copy = write.copy_a600(answer)
        df = rec.reco_a600()[answer][['contentId', 'facltNm', 'firstImageUrl']]
        df = pd.merge(df, self.algopoint, how='left', on='contentId')
        df = df.sort_values('algopoint', ascending=False)[:row]
        return [copy, df]

    def mix_s101(self, row=None):
        copy = write.copy_mix_scene(101)
        merge_df = pd.merge(self.main_a200(1)[1], self.main_a500(1)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s102(self, row=None):
        copy = write.copy_mix_scene(102)
        merge_df = pd.merge(self.main_a410(2)[1], self.main_a600(2)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s103(self, row=None):
        copy = write.copy_mix_scene(103)
        merge_df = pd.merge(self.main_a420(2)[1], self.main_a500(3)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s104(self, row=None):
        copy = write.copy_mix_scene(104)
        merge_df = pd.merge(self.main_a420(1)[1], self.main_a600(3)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s105(self, row=None):
        copy = write.copy_mix_scene(105)
        merge_df = pd.merge(self.main_a500(4)[1], self.main_a600(3)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s106(self, row=None):
        copy = write.copy_mix_scene(106)
        merge_df = pd.merge(self.main_a200(3)[1], self.main_a500(2)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s107(self, row=None):
        copy = write.copy_mix_scene(107)
        merge_df = pd.merge(self.main_a410(3)[1], self.main_a500(2)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s108(self, row=None):
        copy = write.copy_mix_scene(108)
        merge_df = pd.merge(self.main_a410(3)[1], self.main_a420(2)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s109(self, row=None):
        copy = write.copy_mix_scene(109)
        merge_df = pd.merge(self.main_a200(1)[1], self.main_a500(3)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s110(self, row=None):
        copy = write.copy_mix_scene(110)
        merge_df = pd.merge(self.main_a420(1)[1], self.main_a500(3)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s111(self, row=None):
        copy = write.copy_mix_scene(111)
        merge_df = pd.merge(self.main_a210(1)[1], self.main_a500(2)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s112(self, row=None):
        copy = write.copy_mix_scene(112)
        merge_df = pd.merge(self.main_a420(1)[1], self.main_a600(6)[1], how='left', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s113(self, row=None):
        copy = write.copy_mix_scene(113)
        merge_df = pd.merge(self.main_a500(4)[1], self.main_a600(6)[1], how='left', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s114(self, row=None):
        copy = write.copy_mix_scene(114)
        merge_df = pd.merge(self.main_a500(3)[1], self.main_a600(6)[1], how='left', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s115(self, row=None):
        copy = write.copy_mix_scene(115)
        merge_df = pd.merge(self.main_a200(1)[1], self.main_a300(1)[1], how='left', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s116(self, row=None):
        copy = write.copy_mix_scene(116)
        merge_df = pd.merge(self.main_a200(2)[1], self.main_a300(1)[1], how='right', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s117(self, row=None):
        copy = write.copy_mix_scene(117)
        merge_df = pd.merge(self.main_a200(1)[1], self.main_a300(2)[1], how='left', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s118(self, row=None):
        copy = write.copy_mix_scene(118)
        merge_df = pd.merge(self.main_a200(2)[1], self.main_a300(2)[1], how='left', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df

    def mix_s119(self, row=None):
        copy = write.copy_mix_scene(119)
        merge_df = pd.merge(self.main_a200(3)[1], self.main_a300(2)[1], how='left', on='contentId')
        df = self.mix_merge(merge_df, row=row)
        return copy, df


if __name__ == '__main__':
    db = AccessDb()
    # result_df = db.read_user_db(63)
    # print(result_df)
    # answer_ls = db.get_answer_ls(63)
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

    # [copy200, df200] = scene.main_a200(answer_ls[0])
    # [copy210, df210] = scene.main_a210(answer_ls[1])
    # [copy300, df300] = scene.main_a300(answer_ls[2])
    # [copy410, df410] = scene.main_a410(answer_ls[3])
    # [copy420, df420] = scene.main_a420(answer_ls[4])
    # [copy500, df500] = scene.main_a500(answer_ls[5])
    # [copy600, df600] = scene.main_a600(answer_ls[6])

    # print(copy200)
    # print(df200.columns)
    # print(len(df200))
    # print(df200)

    copy_s, df_s = scene.mix_s119(row=20)
    print(copy_s)
    print(df_s.columns)
    print(len(df_s))
    print(df_s)

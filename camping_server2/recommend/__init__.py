import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))
import camping_server2.db.sql_create as sc
import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
import pandas as pd
import numpy as np



class Recommend:
    def __init__(self):
        sql = sc.Query()
        self.IP = sql.IP
        self.DB = sql.DB
        self.PW = sql.PW

    def read_db(self):
        """DB.user 테이블에서 유저가 등록한 응답 불러오기"""
        sql = Query()
        cursor, engine, db = sql.connect_sql()
        query = "select * from user"
        cursor.execute(query)
        result = cursor.fetchall()
        result_df = pd.DataFrame(result)
        result_df = result_df[['id', 'A100', 'A200', 'A210', 'A300', 'A410', 'A420', 'A500', 'A600']].copy()
        result_df.set_index('id', drop=True, inplace=True)
        return result_df

    def get_answer_ls(self, id):
        result_df = self.read_db()
        answer_ls = result_df.loc[id].tolist()
        return answer_ls


if __name__ == '__main__':
    rec = Recommend()
    result_df = rec.read_db()
    print(result_df)
    answer_ls = get_answer_ls(63)
    print(63)
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import algostar.algo_points as aap
import algostar.tag_points as atp
algo = aap.AlgoPoints()
tag = atp.TagPoints()
pymysql.install_as_MySQLdb()


class CreateDb:
    def __init__(self):
        pass

    def create_result_tb(self, db, table, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.{table};
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
        create table {db}.{table} (
            content_id  VARCHAR(5)   PRIMARY KEY,
            place_name  VARCHAR(50)  NOT NULL,
            comfort     FLOAT        NOT NULL,     CHECK(comfort <= 100 and comfort >= 0),
            together    FLOAT        NOT NULL,     CHECK(together <= 100 and together >= 0),
            fun         FLOAT        NOT NULL,     CHECK(fun <= 100 and fun >= 0),
            healing     FLOAT        NOT NULL,     CHECK(healing <= 100 and healing >= 0),
            clean       FLOAT        NOT NULL,     CHECK(clean <= 100 and clean >= 0),
            tag1        VARCHAR(20)  NULL,
            tag_point1  FLOAT        NULL,         CHECK(tag_point1 >= tag_point2),
            tag2        VARCHAR(20)  NULL,
            tag_point2  FLOAT        NULL,         CHECK(tag_point2 >= tag_point3),
            tag3        VARCHAR(20)  NULL,
            tag_point3  FLOAT        NULL,         CHECK(tag_point3 >= tag_point4),
            tag4        VARCHAR(20)  NULL,
            tag_point4  FLOAT        NULL,         CHECK(tag_point4 >= tag_point5),
            tag5        VARCHAR(20)  NULL,
            tag_point5  FLOAT        NULL
            );
            ''')
        cursor.execute(qry_result)

        qry_charset = (f'''
                        alter table {db}.{table} convert to charset utf8;
                       ''')
        cursor.execute(qry_charset)

        qry_check_one = ('''
                SET foreign_key_checks = 1;
                ''')
        cursor.execute(qry_check_one)

class MakeDataframe:
    def __init__(self):
        pass

    def make_result_df(self):
        tag_df = tag.make_tag_prior_df()
        point_df = algo.make_algo_df()
        result_df = pd.merge(point_df, tag_df, on='contentId')
        result_df.rename(columns={
            'contentId': 'content_id',
            'camp': 'place_name'
             }, inplace=True)
        print(result_df.columns)
        return result_df


class Query:
    def __init__(self):
        self.IP = ''
        self.DB = ''
        self.PW = ''

    # db cursor 생성
    def connect_sql(self):
        engine = create_engine(f"mysql+mysqldb://root:{self.PW}@{self.IP}/{self.DB}?charset=utf8", encoding='utf-8')

        conn = engine.connect()

        mydb = pymysql.connect(
            user='root',
            passwd=self.PW,
            host=self.IP,
            db=self.DB,
            use_unicode=True,
            charset='utf8',
        )
        cursor = mydb.cursor(pymysql.cursors.DictCursor)
        return cursor, engine, mydb

    # db에 저장
    def save_sql(self, cursor, engine, db, data, table, option):
        data.to_sql(name=table, con=engine, if_exists=option, index=False)


if __name__ == '__main__':
    sql = Query()
    create = CreateDb()
    content = MakeDataframe()

    cursor, engine, db = sql.connect_sql()
    create.create_result_tb(sql.DB, 'result', cursor)
    result_df = content.make_result_df()
    sql.save_sql(cursor, engine, db, result_df, 'result', 'append')

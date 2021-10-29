import pandas as pd
import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from ..model.connect import Query as sc


class Visitor(sc):
    def __init__(self):
        super().__init__()
        self.cursor, self.engine, self.mydb = self.connect_sql()

    def read_visitor_db(self, start_ymd, end_ymd):
        query = f"(SELECT * FROM {self.DB}.visitor_past\
                  WHERE base_ymd BETWEEN '{start_ymd}' and '{end_ymd}')\
                  UNION ALL\
                 (SELECT sigungu_code, base_ymd, visitor FROM {self.DB}.visitor_future\
                  WHERE base_ymd  BETWEEN '{start_ymd}' and '{end_ymd}');"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        result_df = pd.DataFrame(result)
        # print(len(result_df), result_df.columns)
        return result_df

    def date_list(self):
        today = datetime.datetime.today()
        date_ls = []
        for day in range(-4, 5):
            date = str(today + datetime.timedelta(days=day))[:10]
            date_ls.append(date)
        # print(f"today is {str(today)[:10]} / date list: {date_ls}")
        return date_ls

    def visitor_avg(self):
        df = self.read_visitor_db(self.date_list()[0], self.date_list()[-1])[['base_ymd', 'visitor']]
        avg_df = df.groupby('base_ymd').mean().round()
        avg_df.rename(columns={'visitor': 'avg_visitor'}, inplace=True)
        return avg_df

    def visitor_sigungu(self, sigungu):
        df = self.read_visitor_db(self.date_list()[0], self.date_list()[-1])
        df = df[df['sigungu_code'] == sigungu][['base_ymd', 'visitor']]
        sgg_df = df.groupby('base_ymd').mean().round()
        sgg_df.rename(columns={'visitor': 'sgg_visitor'}, inplace=True)
        return sgg_df

    def visitor_final(self, sigungu):
        avg_df = self.visitor_avg()
        sgg_df = self.visitor_sigungu(sigungu)
        visitor_df = pd.concat([avg_df, sgg_df], axis=1)
        return visitor_df
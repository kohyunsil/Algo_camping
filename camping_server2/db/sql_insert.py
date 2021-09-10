import pymysql
from sqlalchemy import create_engine
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm
from fbprophet import Prophet
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import camping_server2.config as config
import camping_server2.apis.gocamping_api as ga
import camping_server2.apis.koreatour_api as ka
import camping_server2.apis.make_sigungucode as sg
import camping_server2.algostar.algo_points as aap
import camping_server2.algostar.tag_points as atp
gocamp = ga.GocampingApi()
tourapi = ka.KoreaTourApi()
sgg = sg.Sigungucode()
algo = aap.AlgoPoints()
tag = atp.TagPoints()
pymysql.install_as_MySQLdb()


class MakeDataframe:
    def __init__(self):
        self.DIMENSION = config.Config.WEIGHTS
        self.SIGUNGU = config.Config.SIGUNGU
        self.camp = config.Config.CAMP gocamp.gocampingAPI()
        self.festival = config.Config.FESTIVAL  # tourapi.festivalAPI(20210820)
        self.tour = config.Config.TOUR
        self.camp_details = config.Config.CAMP_DETAILS

    def make_camp_df(self):
        # 캠핑장, 축제, 관광지 전처리
        camp = self.camp[['addr1', 'contentId', 'createdtime', 'firstImageUrl', 'homepage',
                          'induty', 'intro', 'mapX', 'lineIntro', 'mapY', 'modifiedtime', 'operDeCl',
                          'operPdCl', 'facltNm', 'tel', 'themaEnvrnCl',
                          'tourEraCl', 'animalCmgCl']].copy()
        # 시군구코드 추가
        camp = sgg.make_sigungucode(camp)

        # 컬럼명 DB 삽입용으로 변경
        camp = camp.rename(columns={'addr1': 'addr',
                                    'animalCmgCl': 'animal_cmg',
                                    'contentId': 'content_id',
                                    'createdtime': 'created_date',
                                    'facltNm': 'place_name',
                                    'induty': 'industry',
                                    'mapX': 'lat',
                                    'mapY': 'lng',
                                    'modifiedtime': 'modified_date',
                                    'operDeCl': 'oper_date',
                                    'operPdCl': 'oper_pd',
                                    'firstImageUrl': 'first_image',
                                    'themaEnvrnCl': 'thema_envrn',
                                    'tourEraCl': 'tour_era',
                                    'lineIntro': 'line_intro',
                                    'sigungucode': 'sigungu_code',
                                    })
        # 캠핑장 크롤링 데이터 전처리
        camp_details = self.camp_details.rename(columns={'view': 'readcount'})
        camp_details['readcount'] = camp_details['readcount'].str.split(' ').str[1]
        datas = camp_details['link']
        data = [re.findall("\d+", data)[0] for data in datas]
        camp_details['url_num'] = data
        # camp_details['url_num'] = camp_details['url_num'].astype('int')
        # 캠핑장 크롤링 과 API 데이터 merge
        merge_data = pd.merge(camp, camp_details, how='left', left_on='content_id', right_on='url_num')
        merge_data.drop(['title', 'address', 'url_num', 'description'], 1, inplace=True)
        merge_data.dropna(subset=['addr'], inplace=True)
        merge_data = merge_data.rename(columns={
                                          'link': 'detail_image',
                                          'tags': 'tag',
                                          'view': 'readcount',
                                          })
        return merge_data

    def make_tourspot_df(self):
        festival = self.festival.drop(['addr2', 'areacode', 'cat1', 'cat2', 'cat3', 'contenttypeid', 'mlevel', "firstimage2",
                                       "createdtime", "modifiedtime", 'tel'], 1)
        tour = self.tour.drop(['addr2', 'areacode', 'booktour', 'cat1', 'cat2', 'cat3', 'contenttypeid', 'mlevel',
                               'zipcode', "firstimage2", 'tel'], 1)
        festival = festival.rename(columns={'addr1': 'addr',
                                            'contentid': 'content_id',
                                            'eventenddate': 'event_end_date',
                                            'eventstartdate': 'event_start_date',
                                            'firstimage': 'first_image',
                                            'mapx': 'lat',
                                            'mapy': 'lng',
                                            'sigungucode': 'sigungu_code',
                                            'title': 'place_name'})
        festival['place_num'] = 1
        tour = tour.rename(columns={'addr1': 'addr',
                                    'contentid': 'content_id',
                                    'firstimage': 'first_image',
                                    'mapx': 'lat',
                                    'mapy': 'lng',
                                    'sigungucode': 'sigungu_code',
                                    'title': 'place_name'})
        tour['place_num'] = 0

        data = pd.concat([tour, festival], 0)
        data = data.dropna(subset=['addr'])
        data = data.reset_index()
        # data.index = data.index + 1
        # data['place_id'] = data.index
        data = data.drop(['index'], 1)
        data = data.rename(columns={'img_url': 'detail_image',
                                    'tags': 'tag',
                                    'view': 'readcount'})

        return data

    def make_dimension_df(self):
        return self.DIMENSION

    def make_sigungu_df(self):
        self.SIGUNGU.rename(columns={
            'signguCode': 'sigungu_code',
            'areaNm': 'area_name',
            'signguNm': 'sigungu_name'
        }, inplace=True)
        self.SIGUNGU.drop('areaCode', axis=1, inplace=True)
        return self.SIGUNGU

    def make_algopoint_df(self):
        point_df = algo.make_algo_df()
        point_df.rename(columns={
            'contentId': 'content_id'
        }, inplace=True)
        point_df.drop('camp', axis=1, inplace=True)
        print(point_df.columns)
        return point_df

    def make_algotag_df(self):
        tag_df = tag.make_tag_prior_df()
        tag_df.rename(columns={
            'contentId': 'content_id'
        }, inplace=True)
        print(tag_df.columns)
        return tag_df

    def make_visitor_past_df(self, startYmd=20180101, endYmd=20210910): #visitor_past_df
        df = tourapi.visitors_API(startYmd, endYmd)
        # df = pd.read_csv("../../datas/visitors_2018_2021.csv", index_col=[0], encoding='utf-8-sig')
        df.replace(to_replace=0, value=0.0001, inplace=True)  # 0명의 경우 근사치인 0.0001로 치환
        result_df = df[['baseYmd', 'signguCode', 'signguNm', 'touDivNm', 'touNum']].copy()
        idx = df[df['touDivNm'] == '현지인(a)'].index
        result_df.drop(idx, inplace=True)
        result_df = result_df.groupby(by=['baseYmd', 'signguCode', 'signguNm']).sum()
        result_df.reset_index(inplace=True)
        result_df['baseYmd'] = result_df['baseYmd'].astype(str)
        result_df['baseYmd'] = pd.to_datetime(result_df['baseYmd'], format='%Y-%m-%d')
        result_df.sort_values(by=['signguCode', 'baseYmd'], inplace=True)
        result_df['signguCode'] = result_df['signguCode'].replace(28170, 28177)
        result_df.reset_index(drop=True, inplace=True)

        result_df.rename(columns={
            'baseYmd': 'base_ymd',
            'signguCode': 'sigungu_code',
            'touNum': 'visitor'
        }, inplace=True)
        result_df = result_df[['base_ymd', 'sigungu_code', 'visitor']].copy()
        return result_df

    def make_visitor_future_df(self, startYmd=20180101, endYmd=20210910, period=90):
        sql = Query()
        cursor, engine, db = sql.connect_sql()
        query = "select * from visitor_past"
        cursor.execute(query)
        result = cursor.fetchall()
        result_df = pd.DataFrame(result) #self.make_visitor_past_df(startYmd, endYmd)
        print(result_df.tail())
        sgg_list = np.unique(result_df.sigungu_code).tolist()
        ymd_list = pd.to_datetime(np.unique(result_df.base_ymd).tolist(), format='%Y-%m-%d')

        final_df = pd.DataFrame(index=ymd_list)
        for sgg in tqdm(sgg_list):
            final_df[sgg] = result_df[result_df['sigungu_code'] == sgg]['visitor'].tolist()
        print(f"기간: 총 {len(final_df.index)}일, 시군구 개수: {len(final_df.columns)}")

        predict_df = pd.DataFrame(columns=['ds', 'trend', 'sigungu_code'])
        for sigungu in tqdm(final_df.columns.tolist()):
            train_data = final_df[[sigungu]].copy().reset_index()
            train_data.rename(columns={'index': 'ds', sigungu: 'y'}, inplace=True)
            m = Prophet(seasonality_mode='multiplicative', yearly_seasonality=True, daily_seasonality=True)
            m.fit(train_data)
            future = m.make_future_dataframe(periods=period)
            forecast = m.predict(future)
            new_df = forecast[['ds', 'trend']][-period:].reset_index(drop=True)
            new_df['sigungu_code'] = sigungu
            predict_df = pd.concat([predict_df, new_df], axis=0)
            predict_df.reset_index(drop=True, inplace=True)
            predict_df['created_date'] = datetime.today().strftime("%Y-%m-%d")

        predict_df.rename(columns={
            'ds': 'base_ymd',
            'trend': 'visitor'
        }, inplace=True)

        return predict_df


class Query:
    def __init__(self):
        self.IP = ' '
        self.DB = ' '
        self.PW = ' '

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
    def save_sql(self, engine, data, table, option):
        data.to_sql(name=table, con=engine, if_exists=option, index=False)


if __name__ == '__main__':
    sql = Query()
    cursor, engine, db = sql.connect_sql()

    content = MakeDataframe()
    # dimension_df = content.make_dimension_df()
    # sql.save_sql(engine, dimension_df, 'dimension', 'append')
    #
    # sigungu_df = content.make_sigungu_df()
    # sql.save_sql(engine, sigungu_df, 'sigungu', 'append')

    # camp_df = content.make_camp_df()
    # print(camp_df.columns)
    # camp_df.to_csv("let me see.csv", encoding='utf-8-sig')
    # sql.save_sql(engine, camp_df, 'camp', 'append')
    # tourspot_df = content.make_tourspot_df()
    # print(tourspot_df.columns)
    # sql.save_sql(engine, tourspot_df, 'tourspot', 'append')
    # algopoint_df = content.make_algopoint_df()
    # sql.save_sql(engine, algopoint_df, 'algopoint', 'append')


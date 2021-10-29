import pymysql
from sqlalchemy import create_engine
import re
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
from fbprophet import Prophet
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))
import camping_server2.config as config
import camping_server2.apis.gocamping_api as ga
import camping_server2.apis.koreatour_api as ka
import camping_server2.apis.make_sigungucode as sg
import camping_server2.algostar.algo_points as aap
import camping_server2.algostar.tag_points as atp
import camping_server2.algostar.camp_api_crawling_merge as cacm
import camping_server2.recommend.recommend_final as rf
gocamp = ga.GocampingApi()
tourapi = ka.KoreaTourApi()
sgg = sg.Sigungucode()
algo = aap.AlgoPoints()
tag = atp.TagPoints()
rv_camp = cacm.ReviewCamp()
pymysql.install_as_MySQLdb()


class MakeDataframe:
    def __init__(self):
        self.category = config.Config.CATEGORY
        self.DIMENSION = config.Config.WEIGHTS
        self.SIGUNGU = config.Config.SIGUNGU
        self.camp = gocamp.gocampingAPI()  # config.Config.CAMP
        self.festival = config.Config.FESTIVAL  # tourapi.festivalAPI(20210820)
        self.tour = config.Config.TOUR
        self.camp_details = config.Config.CAMP_DETAILS

    def make_camp_df(self, last_date='0'):  # '2021-09-01 00:00:00'
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

        # 캠핑장 크롤링 과 API 데이터 merge
        camp_details = self.camp_details
        camp_details['contentId'] = camp_details['contentId'].astype(str)
        merge_data = pd.merge(camp, camp_details, how='left', on='contentId')
        merge_data.dropna(subset=['addr'], inplace=True)
        merge_data = merge_data.rename(columns={
                                          'link': 'detail_image',
                                          'tags': 'tag',
                                          'view': 'readcount',
                                          'contentId': 'content_id'
                                          })

        merge_data = merge_data[merge_data['created_date'] > last_date]
        merge_data.drop_duplicates(subset=['content_id'], inplace=True)
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

        scale = point_df.iloc[:, 2:]
        log_df1 = np.log1p(scale)
        dec_max = 100 / (log_df1.max().max())
        log_df2 = np.log1p(scale) * dec_max
        scaled_df = pd.concat([point_df.iloc[:, :2], log_df2], 1)

        point_df.drop('camp', axis=1, inplace=True)
        point_df.set_index('contentId', inplace=True)
        point_df['algostar'] = np.round(scaled_df.sum(axis=1)/100, 1)
        point_df.reset_index(inplace=True)
        point_df.rename(columns={
            'contentId': 'content_id'
        }, inplace=True)
        print(point_df.columns)
        return point_df

    def make_algotag_df(self):
        tag_df = tag.make_tag_prior_df()
        tag_df.rename(columns={
            'contentId': 'content_id',
            'total_points': 'point'
        }, inplace=True)
        print(tag_df.columns)
        return tag_df

    def make_feature_df(self, last_date='0'):
        camp_df = self.make_camp_df(last_date)
        camp_df2 = camp_df[['content_id', 'addr']].copy()
        algo_result = rv_camp.review_camp_merge()
        algo_result.rename(columns={
                              'camp': 'place_name',
                              'contentId': 'content_id',
                              'insrncAt': 'insrnc_at',
                              'trsagntNo': 'trsagnt_no',
                              'mangeDivNm': 'mange',
                              'manageNmpr': 'manage_num',
                              'sitedStnc': 'sited_stnc',
                              'glampInnerFclty': 'glampinner_fclty',
                              'caravInnerFclty': 'caravinner_fclty',
                              'trlerAcmpnyAt': 'trler_acmpny',
                              'caravAcmpnyAt': 'carav_acmpny',
                              'swrmCo': 'swrm_cnt',
                              'toiletCo': 'toilet_cnt',
                              'wtrplCo': 'wtrpl_cnt',
                              'brazierCl': 'brazier',
                              'sbrsCl': 'sbrs',
                              'sbrsEtc': 'sbrs_etc',
                              'posblFcltyCl': 'posblfclty',
                              'extshrCo': 'extshr',
                              'frprvtWrppCo': 'frprvtwrpp',
                              'frprvtSandCo': 'frprvtsand',
                              'fireSensorCo': 'firesensor',
                              'animalCmgCl': 'animal_cmg'
                            }, inplace=True)
        algo_result['content_id'] = algo_result['content_id'].astype(str)
        merge_data = pd.merge(algo_result, camp_df2, how='left', on='content_id')
        merge_data.drop(['menu_r', 'food_amount_r'], axis=1, inplace=True)

        camping_data = camp_df[['content_id', 'addr', 'tag', 'animal_cmg']].copy()
        camping_data['tag'] = camping_data['tag'].fillna("")

        # 반려견 출입 가능 유무 컬럼으로 반려견 태그 만들기
        camping_data["tag"][camping_data["animal_cmg"] == "가능"] = camping_data[camping_data["animal_cmg"] == "가능"][
                                                                      "tag"] + "#반려견"
        camping_data["tag"][camping_data["animal_cmg"] == "가능(소형견)"] = \
        camping_data[camping_data["animal_cmg"] == "가능(소형견)"]["tag"] + "#반려견"

        # 태그 내에서 봄,여름,가을,겨울 제외
        camping_data['tag'] = [t[:] if type(t) == str else "" for t in camping_data['tag']]
        for kw in [',', '#봄 ', '#여름 ', '#가을', '#겨울', '봄', '여름', '가을', '겨울']:
            camping_data['tag'] = [t.replace(kw, "") if type(t) == str else np.NaN for t in camping_data['tag']]
        # 소분류 one hot encoding
        camping_data["tag"] = camping_data["tag"].str.replace(" #", "#")
        subcat = camping_data["tag"].str.split("#").apply(pd.Series).loc[:, 1:]
        sub_df = pd.get_dummies(subcat.stack()).reset_index().groupby("level_0").sum().drop("level_1", 1)
        sub_df.drop("", axis=1, inplace=True)
        sub_df.index = sub_df.index.astype(str)

        lookup = pd.DataFrame(columns=["sub_cat", "main_cat"], data=list(self.category.items()))
        lookup['main_cat'] = lookup['main_cat'].str.replace(" ", "")

        # 5개 대분류 one hot encoding
        main_df = pd.DataFrame()
        for i in range(len(sub_df)):
            main_df = pd.concat([pd.DataFrame(sub_df.values[i] * lookup["main_cat"].T), main_df], 1)
        main_df = main_df.T.reset_index(drop=True)
        main_df = pd.get_dummies(main_df.stack()).reset_index().groupby("level_0").sum().drop("level_1", 1)
        main_df = main_df.iloc[:, 1:]
        main_df.index = sub_df.index
        main_df.index = main_df.index.astype(str)
        main_df = pd.merge(main_df, sub_df[['반려견']], how='left', left_index=True, right_index=True)
        main_df.reset_index(inplace=True)
        main_df.rename(columns={'level_0': 'content_id',
                                '반려견': 'with_pet_s',
                                '액티비티': 'activity_m',
                                '자연/힐링': 'nature_m',
                                '즐길거리': 'fun_m',
                                '쾌적/편리': 'comfort_m',
                                '함께': 'together_m'}, inplace=True)

        final_data = pd.merge(merge_data, main_df, how='left', on='content_id')
        print(len(final_data.columns), final_data.columns)

        return final_data

    def make_visitor_past_df(self, startYmd=20180101, endYmd=20211019): #visitor_past_df
        # df = tourapi.visitors_API(startYmd, endYmd)
        df = pd.read_csv("../../datas/past_visitors_20211028.csv", index_col=[0], encoding='utf-8-sig')
        df.replace(to_replace=0, value=0.0001, inplace=True)  # 0명의 경우 근사치인 0.0001로 치환
        result_df = df[['baseYmd', 'signguCode', 'signguNm', 'touDivNm', 'touNum']].copy()
        idx = df[df['touDivNm'] == '현지인(a)'].index
        result_df.drop(idx, inplace=True)
        result_df = result_df.groupby(by=['baseYmd', 'signguCode', 'signguNm']).sum()
        result_df.reset_index(inplace=True)
        result_df['baseYmd'] = result_df['baseYmd'].astype(str)
        result_df['baseYmd'] = pd.to_datetime(result_df['baseYmd'], format='%Y-%m-%d')
        result_df.sort_values(by=['signguCode', 'baseYmd'], inplace=True)
        result_df['signguCode'] = result_df['signguCode'].replace({28170: 28177})
        result_df.reset_index(drop=True, inplace=True)

        result_df.rename(columns={
            'baseYmd': 'base_ymd',
            'signguCode': 'sigungu_code',
            'touNum': 'visitor'
        }, inplace=True)
        result_df = result_df[['base_ymd', 'sigungu_code', 'visitor']].copy()
        return result_df

    def make_visitor_future_df(self, startYmd, endYmd, period=90):
        # sql = Query()
        # cursor, engine, db = sql.connect_sql()
        # query = f"select * from {sql.DB}.visitor_past"
        # cursor.execute(query)
        # result = cursor.fetchall()
        result_df = self.make_visitor_past_df(startYmd, endYmd)  # pd.DataFrame(result)
        result_df['sigungu_code'] = result_df['sigungu_code'].replace({28170: 28177})
        print(result_df.tail())
        sgg_list = np.unique(result_df.sigungu_code.tolist())
        ymd_list = np.unique(result_df.base_ymd.tolist())
        ymd_list = [pd.to_datetime(ymd, format='%Y-%m-%d') for ymd in ymd_list]
        print(f"총 시군구 개수: {len(sgg_list)}")
        print(f"기간: 총 {len(ymd_list)}일 / 시작일: {ymd_list[0]} / 종료일: {ymd_list[-1]}")

        final_df = pd.DataFrame(index=ymd_list)
        for sgg in tqdm(sgg_list):
            final_df[sgg] = result_df[result_df['sigungu_code'] == sgg]['visitor'].tolist()
        print(f"기간: 총 {len(final_df.index)}일, 시군구 개수: {len(final_df.columns)}")

        predict_df = pd.DataFrame(columns=['ds', 'yhat', 'sigungu_code'])
        for sigungu in tqdm(final_df.columns.tolist()):
            train_data = final_df[[sigungu]].copy().reset_index()
            train_data.rename(columns={'index': 'ds', sigungu: 'y'}, inplace=True)
            m = Prophet(seasonality_mode='multiplicative', yearly_seasonality=True, daily_seasonality=True)
            m.fit(train_data)
            future = m.make_future_dataframe(periods=period)
            forecast = m.predict(future)
            new_df = forecast[['ds', 'yhat']][-period:].reset_index(drop=True)
            new_df['sigungu_code'] = sigungu
            predict_df = pd.concat([predict_df, new_df], axis=0)
            predict_df.reset_index(drop=True, inplace=True)

        predict_df = predict_df[['sigungu_code', 'ds', 'yhat']].copy()
        predict_df['created_date'] = datetime.now()
        predict_df.rename(columns={
            'ds': 'base_ymd',
            'yhat': 'visitor'
        }, inplace=True)

        return predict_df

    def make_review_df(self):
        path = config.Config.PATH
        kakao = pd.read_csv(path + "kakao_review_cat_predict.csv", encoding='utf-8-sig', low_memory=False)
        naver = pd.read_csv(path + "v5_category_re.csv", encoding='utf-8-sig', low_memory=False)

        # 카카오 리뷰 전처리
        kakao['platform'] = 0
        kakao = kakao.rename(columns={'kakaoMapUserId': 'user_id',
                                      'point': 'star',
                                      'likeCnt': 'like_cnt',
                                      'photoCnt': 'photo_cnt',
                                      'username': 'user_nickname',
                                      'category': 'cat_tag'})

        # 네이버 리뷰 전처리
        naver['user_info'] = naver['user_info'].str.replace("\n", "")
        naver['user_info'] = naver['user_info'].str.replace(" ", "")
        naver["user_review"] = \
        naver['user_info'].str.split("리뷰", expand=True)[1].str.split("평균별점", expand=True)[0].str.split("사진",
                                                                                                       expand=True)[0]
        naver["user_picture"] = naver['user_info'].str.split("사진", expand=True)[1].str.split("평균별점", expand=True)[0]
        naver["user_star"] = naver['user_info'].str.split("평균별점", expand=True)[1]
        naver['date'], naver['visit'] = naver["visit_info"].str.split(" ", 1).str
        naver['visit_date'] = naver['date'].str[:10]
        naver = naver.drop(['user_info', 'visit_info', 'date', 'visit'], 1)
        naver['platform'] = 1
        naver = naver.drop(['addr'], 1)
        naver = naver.rename(columns={'title': 'place_name',
                                      'user_name': 'user_nickname',
                                      'visit_date': 'date',
                                      'base_addr': 'addr',
                                      'user_picture': 'photo_cnt',
                                      'highlight_review': 'contents',
                                      'category': 'cat_tag',
                                      'user_review': 'review_cnt',
                                      'user_star': 'mean_star'})

        # 카카오 + 네이버 MERGE
        kakao_naver = pd.concat([naver, kakao], 0)
        review_data = self.camp[['contentId', 'facltNm']].copy()
        review_data = review_data.rename(columns={'contentId': 'camp_id', 'facltNm': 'place_name'})
        review_data_df = pd.merge(review_data, kakao_naver, left_on='place_name', right_on='place_name', how="right")
        review_data_df = review_data_df.drop_duplicates()
        review_data_df = review_data_df.reset_index()
        review_data_df = review_data_df.rename(columns={'index': 'id', 'userId': 'user_id'})
        review_df = review_data_df[['platform', 'user_id', 'camp_id', 'photo_cnt', 'date', 'cat_tag', 'star', 'contents']]
        review_df = review_df.dropna(subset=['camp_id'])
        return review_df

    def make_scenario_df(self, row=20):
        scene = rf.Scenario()
        ### Main Scenario
        row = 20
        main_scene_dict = {'a200': [i for i in range(1, 5)],  # a200
                           'a210': [1],  # a210 - 반려동물 동반 O만 대상
                           'a300': [i for i in range(1, 4)],  # a300
                           'a410': [i for i in range(1, 5)],  # a410
                           'a420': [i for i in range(1, 5)],  # a420
                           'a500': [i for i in range(1, 5)],  # a500
                           'a600': [i for i in range(1, 7)]}  # a600

        result_df2 = pd.DataFrame()
        for ans in main_scene_dict['a200']:
            df = scene.main_a200(ans, row)[1][['contentId', 'facltNm', 'firstImageUrl']]
            df['scene_no'] = 'a200'
            df['copy'] = scene.main_a200(ans, row)[0]
            df['a200'] = ans
            result_df2 = pd.concat([result_df2, df])

        for ans in main_scene_dict['a210']:
            df = scene.main_a210(ans, row)[1][['contentId', 'facltNm', 'firstImageUrl']]
            df['scene_no'] = 'a210'
            df['copy'] = scene.main_a210(ans, row)[0]
            df['a210'] = ans
            result_df2 = pd.concat([result_df2, df])

        for ans in main_scene_dict['a300']:
            df = scene.main_a300(ans, row)[1][['contentId', 'facltNm', 'firstImageUrl']]
            df['scene_no'] = 'a300'
            df['copy'] = scene.main_a300(ans, row)[0]
            df['a300'] = ans
            result_df2 = pd.concat([result_df2, df])

        for ans in main_scene_dict['a410']:
            df = scene.main_a410(ans, row)[1][['contentId', 'facltNm', 'firstImageUrl']]
            df['scene_no'] = 'a410'
            df['copy'] = scene.main_a410(ans, row)[0]
            df['a410'] = ans
            result_df2 = pd.concat([result_df2, df])

        for ans in main_scene_dict['a420']:
            df = scene.main_a420(ans, row)[1][['contentId', 'facltNm', 'firstImageUrl']]
            df['scene_no'] = 'a420'
            df['copy'] = scene.main_a420(ans, row)[0]
            df['a420'] = ans
            result_df2 = pd.concat([result_df2, df])

        for ans in main_scene_dict['a500']:
            df = scene.main_a500(ans, row)[1][['contentId', 'facltNm', 'firstImageUrl']]
            df['scene_no'] = 'a500'
            df['copy'] = scene.main_a500(ans, row)[0]
            df['a500'] = ans
            result_df2 = pd.concat([result_df2, df])

        for ans in main_scene_dict['a600']:
            df = scene.main_a600(ans, row)[1][['contentId', 'facltNm', 'firstImageUrl']]
            df['scene_no'] = 'a600'
            df['copy'] = scene.main_a600(ans, row)[0]
            df['a600'] = ans
            result_df2 = pd.concat([result_df2, df])

        result_df2['spot1'] = 1
        result_df2['spot2'] = 0

        ### Mix Scenario
        scene_dict = {'s101': scene.mix_s101(row=row),
                      's102': scene.mix_s102(row=row),
                      's103': scene.mix_s103(row=row),
                      's104': scene.mix_s104(row=row),
                      's105': scene.mix_s105(row=row),
                      's106': scene.mix_s106(row=row),
                      's107': scene.mix_s107(row=row),
                      's108': scene.mix_s108(row=row),
                      's109': scene.mix_s109(row=row),
                      's110': scene.mix_s110(row=row),
                      's111': scene.mix_s111(row=row),
                      's112': scene.mix_s112(row=row),
                      's113': scene.mix_s113(row=row),
                      's114': scene.mix_s114(row=row),
                      's115': scene.mix_s115(row=row),
                      's116': scene.mix_s116(row=row),
                      's117': scene.mix_s117(row=row),
                      's118': scene.mix_s118(row=row),
                      's119': scene.mix_s119(row=row)}

        que_dict = {'s101': [None, 1, None, None, None, None, 1, None],
                    's102': [None, None, None, None, 2, None, None, 2],
                    's103': [None, None, None, None, None, 2, 3, None],
                    's104': [None, None, None, None, None, 1, None, 3],
                    's105': [None, None, None, None, None, None, 4, 3],
                    's106': [None, 3, None, None, None, None, 2, None],
                    's107': [None, None, None, None, 3, None, 2, None],
                    's108': [None, None, None, None, 3, 2, None, None],
                    's109': [None, 1, None, None, None, None, 3, None],
                    's110': [None, None, None, None, None, 3, 3, None],
                    's111': [None, None, 1, None, None, None, 2, None],
                    's112': [None, None, None, None, None, 1, None, 6],
                    's113': [None, None, None, None, None, None, 4, 6],
                    's114': [None, None, None, None, None, None, 3, 6],
                    's115': [None, 1, None, 1, None, None, None, None],
                    's116': [None, 2, None, 1, None, None, None, None],
                    's117': [None, 1, None, 2, None, None, None, None],
                    's118': [None, 2, None, 2, None, None, None, None],
                    's119': [None, 3, None, 2, None, None, None, None]}
        result_df1 = pd.DataFrame()
        for scene_no in ['s101', 's102', 's105', 's107', 's111', 's112', 's115', 's119']:
            df = scene_dict[scene_no][1]
            df['scene_no'] = scene_no
            df['copy'] = scene_dict[scene_no][0]
            df['spot1'] = 0
            df['spot2'] = 1
            df['a100'] = que_dict[scene_no][0]
            df['a200'] = que_dict[scene_no][1]
            df['a210'] = que_dict[scene_no][2]
            df['a300'] = que_dict[scene_no][3]
            df['a410'] = que_dict[scene_no][4]
            df['a420'] = que_dict[scene_no][5]
            df['a500'] = que_dict[scene_no][6]
            df['a600'] = que_dict[scene_no][7]
            result_df1 = pd.concat([result_df1, df])

        ### Main + Mix Scenario
        result_df = pd.concat([result_df2, result_df1])
        result_df = result_df.rename(columns={'contentId': 'content_id',
                                              'facltNm': 'place_name',
                                              'firstImageUrl': 'first_image'})
        result_df.dropna(axis=0, subset=['first_image', 'copy'], inplace=True)
        return result_df




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

    feature_df = content.make_feature_df()
    sql.save_sql(engine, feature_df, 'feature', 'append')



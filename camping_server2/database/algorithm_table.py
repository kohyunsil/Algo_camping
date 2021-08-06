import pandas as pd
from datetime import date

from pandas.core.indexes import category
import config as config
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler, MaxAbsScaler
from main_table import MainInsert

class AlgoInsert:
    def __init__(self):
        self.category = config.Config.CATEGORY
        self.naver = config.Config.NAVER
        self.kakao = config.Config.KAKAO
        self.camp=config.Config.CAMP
        self.weights=config.Config.WEIGHTS
        self.main_cat=config.Config.MAIN_CAT
    
    # 태그 컬럼 전처리
    def make_tag(self, camp_df):
        camping_data = camp_df[['place_id', 'content_id', 'place_name', 'addr', 'tag', 'animal_cmg']]
        camping_data['tag'] = camping_data['tag'].fillna("")
        # 반려견 출입 가능 유무 컬럼으로 반려견 태그 만들기
        camping_data["tag"][camping_data["animal_cmg"] == "가능"] = camping_data[camping_data["animal_cmg"] == "가능"]["tag"] + "#반려견"
        camping_data["tag"][camping_data["animal_cmg"] == "가능(소형견)"] = camping_data[camping_data["animal_cmg"] == "가능(소형견)"]["tag"] + "#반려견"

        # 태그 내에서 봄,여름,가을,겨울 제외
        camping_data['tag'] = [t[:] if type(t) == str else "" for t in camping_data['tag']]
        for kw in ['#봄 ', '#여름 ', '#가을', '#가을 ', '#겨울', '봄 ', '여름 ', '가을 ', '겨울',]:
            camping_data['tag'] = [t.replace(kw, "") if type(t) == str else "" for t in camping_data['tag']]
        return camping_data
    
    # 소분류 one hot encoding
    def subcat(self, camping_data):
        camping_data["tag"] = camping_data["tag"].str.replace(" ", "")
        subcat = camping_data["tag"].str.split("#").apply(pd.Series).loc[:, 1:]
        sub_df = pd.get_dummies(subcat.stack()).reset_index().groupby("level_0").sum().drop("level_1", 1)
        return sub_df
     
    # 대분류 one hot encoding 
    def maincat(self, sub_df):
        # 대분류 불러오기
        lookup = pd.DataFrame(columns=["sub_cat", "main_cat"], data=self.category)
        lookup['main_cat'] = lookup['main_cat'].str.replace(" ","")

        main_df = pd.DataFrame()
        for i in range(len(sub_df)):
            main_df = pd.concat([pd.DataFrame(sub_df.values[i] * lookup["main_cat"].T), main_df], 1)
        main_df = main_df.T.reset_index(drop=True)
        main_df = pd.get_dummies(main_df.stack()).reset_index().groupby("level_0").sum().drop("level_1", 1)
        main_df = main_df.iloc[:,1:]
        main_df.index = sub_df.index
        return main_df
    
    # 소분류와 대분류 one hot encoding concat
    def make_algo_search(self, camp_df):
        camping_data = self.make_tag(camp_df)
        sub_df = self.subcat(camping_data)
        main_df = self.maincat(sub_df)
        last_df  = pd.concat([sub_df, main_df], 1)
        last_df[last_df > 1] = 1
        last_df['index']= last_df.index
        algo_search_df = pd.merge(camping_data, last_df, how="left", left_on = 'place_id', right_on='index').drop("index", 1)
        algo_search_df = algo_search_df.rename(columns={'가족' : 'with_family_s',
                                            '계곡옆' : 'valley_s',
                                            '깨끗한' : 'clean_s',
                                            '둘레길' : 'trail_s',
                                            '문화유적' : 'cultural_s',
                                            '물놀이하기좋은' : 'waterplay_s',
                                            '물맑은' : 'pure_water_s',
                                            '바다가보이는' : 'ocean_s',
                                            '반려견' : 'with_pet_s',
                                            '별보기좋은' : 'star_s',
                                            '사이트간격이넓은' : 'spacious_s',
                                            '생태교육' : 'ecological_s',
                                            '수영장있는' : 'pool_s',
                                            '아이들놀기좋은' : 'with_child_s',
                                            '온수잘나오는' : 'hot_water_s',
                                            '익스트림' : 'extreme_s',
                                            '자전거타기좋은' : 'bicycle_s',
                                            '차대기편한' : 'parking_s',
                                            '축제' : 'festival_s',
                                            '커플' : 'with_couple_s', 
                                            '힐링' : 'healing_s',
                                            '액티비티' : 'activity_m',
                                            '자연/힐링' : 'nature_m',
                                            '즐길거리' : 'fun_m',
                                            '쾌적/편리' : 'comfort_m',
                                            '함께' : 'together_m'})
        
        return algo_search_df
    
    # 부대시설 등의 컬럼 내역 count 
    def make_count_df(self, camp_df, algo_search_df):
        tmp = camp_df[['content_id', 'insrnc_at', 'trsagnt_no', 'mange', 'manage_num', 'sited_stnc', 'glampinner_fclty', 'caravinner_fclty', 'trler_acmpny', 'carav_acmpny', 'toilet_cnt', 'swrm_cnt', 'wtrpl_cnt', 'brazier', 'sbrs', 'sbrs_etc', 'posblfclty', 'extshr', 'frprvtwrpp', 'frprvtsand', 'firesensor',]]
        is_tmp_df = pd.merge(algo_search_df, tmp, how='left', on='content_id')
        drop_tmp_df = is_tmp_df.drop(['glampinner_fclty', 'caravinner_fclty', 'sbrs', 'sbrs_etc', 'posblfclty'],1)

        count_tmp_df = is_tmp_df[['glampinner_fclty', 'caravinner_fclty', 'sbrs', 'sbrs_etc', 'posblfclty']]
        count_tmp_df = count_tmp_df.apply(lambda x: x.str.count(',') + 1)
        count_tmp_df = count_tmp_df.fillna(0)
        count_tmp_df = count_tmp_df.astype('int')

        count_df = pd.concat([drop_tmp_df, count_tmp_df])
        return count_df

    # reivew 알고리즘용 전처리
    def review_concat(self):
        nv_data = self.naver
        kk_data = self.kakao

        nv_data['user_info'] = nv_data['user_info'].fillna(0)
        nv_data = nv_data[nv_data['user_info'] != 0]
        nv_data['user_info'] = nv_data['user_info'].apply(lambda x: x.split('\n')[-1])
        nv_data['visit_info'] = nv_data['visit_info'].apply(lambda x: x.split('번째')[0][-1])
        nv_data = nv_data[nv_data['star'] != 'star']
        nv_data['star'] = nv_data['star'].astype('float64')
        nv_data['user_info'] = nv_data['user_info'].astype('float64')
        nv_data['visit_info'] = nv_data['visit_info'].astype('float64')
        nv_data = nv_data.drop(['addr', 'base_addr', 'user_name', 'visit_info'], 1)
        nv_data = nv_data.rename(columns={'title': 'camp', 'highlight_review': 'review', 'star': 'point', 'user_info': 'avg_point'})
        nv_data = nv_data[['camp', 'review', 'point', 'category', 'avg_point']]
        nv_data['point'] = nv_data['point'].astype('float64')
        nv_data['avg_point'] = nv_data['avg_point'].astype('float64')

        reviews_df = pd.concat([nv_data, kk_data], 0)
        reviews_df['weights'] = reviews_df['point'] * (reviews_df['point'] / reviews_df['avg_point'])
        reviews_df = reviews_df.reset_index(drop=True)
        return reviews_df

    # 리뷰 스케일링
    def scaling(self):
        reviews_df = self.review_concat()
        rb = RobustScaler()
        rb_df = rb.fit_transform(reviews_df[['weights']])
        rb_df = pd.DataFrame(rb_df)

        rb_df = rb_df.rename(columns={0: 'weights2'})
        rb_df['weights2'] = rb_df['weights2'] * 0.01

        re_df = pd.concat([reviews_df, rb_df], 1)
        re_df['final_point'] = re_df['point'] * (1 + re_df['weights2'])

        mm = MinMaxScaler()
        mm_df = mm.fit_transform(re_df[['final_point']])
        mm_df = pd.DataFrame(mm_df)

        re_df['final_point'] = mm_df * 5
        re_df = re_df.drop(['weights', 'weights2'], 1)
        re_df['final_point'] = round(re_df['final_point'], 1)

        re_df2 = re_df.groupby(['camp', 'category']).mean().reset_index()
        re_df3 = re_df.groupby(['camp', 'category']).size().reset_index(name='count')
        re_df4 = pd.merge(re_df2, re_df3)

        df = re_df4[['camp', 'category', 'final_point']]
        df = pd.pivot_table(df, index='camp', columns='category')
        df = df.fillna(0)
        df = df.reset_index()
        review_result = pd.concat([df["camp"], df["final_point"]], 1)
        return review_result

    # 캠핑장와 리뷰 스케일링 merge
    def merge_dataset(self, review_result):
        review_result = self.scaling()
        
        camp_name = ['느티나무 캠핑장', '늘푸른캠핑장', '두리캠핑장', '둥지캠핑장', '백운계곡캠핑장', '별빛야영장',
             '별헤는 밤', '산여울캠핑장', '소풍캠핑장', '솔바람 캠핑장', '솔밭야영장', '솔밭캠핑장', '포시즌',
             '포시즌 캠핑장']
        for i in camp_name:
            review_result = review_result.query(f'camp != "{i}"')
        merge_result = pd.merge(self.camp, review_result, how='outer', left_on='place_name', right_on='camp')
        result1 = merge_result.iloc[:, 44:].fillna(0)
        result2 = merge_result.iloc[:, :44]
        algo_result = pd.concat([result2, result1], 1)
        return algo_result

    # search table 
    def search_table(self, algo_search_df): 
        search_df = algo_search_df.drop(['place_id','animal_cmg', '재미있는', '친절한', '여유있는', '그늘이많은'],1)
        return search_df

    # algorithm table
    def algorithm_table(self, count_df, algo_result):
        algo_result = algo_result[['content_id', '가격', '만족도',
        '맛', '메인시설', '목적', '부대/공용시설', '분위기', '비품', '서비스', '수영장', '시설물관리',
        '아이 만족도', '예약', '와이파이', '위치', '음식/조식', '입장', '전망', '주차', '즐길거리',
        '청결도', '편의/부대시설', '혼잡도']]
        algo_df = pd.merge(count_df, algo_result, how='left', on='content_id')
        algo_df = algo_df.rename(columns={'id' : 'place_id',
                            '그늘이많은' : 'shade_s',
                            '가격' : 'price_r',
                            '만족도' : 'satisfied_r', 
                                '맛' : 'taste_r',
                                '메인시설' : 'main_r', 
                                '목적' : 'object_r', 
                                '부대/공용시설' : 'facility_r', 
                                '분위기' : 'atmos_r', 
                                '비품' : 'equipment_r', 
                                '서비스' : 'service_r', 
                                '수영장' : 'pool_r', 
                                '시설물관리' : 'manage_r', 
                                '아이 만족도' : 'childlike_r',
                                '예약' : 'reservation_r', 
                                '와이파이' : 'wifi_r', 
                                '위치' : 'location_r', 
                                '음식/조식' : 'food_r', 
                                '입장' : 'enter_r', 
                                '전망' : 'view_r', 
                                '주차' : 'parking_r', 
                                '즐길거리' : 'exciting_r', 
                                '청결도' : 'clean_r', 
                                '편의/부대시설' : 'conv_facility_r',
                                '혼잡도' : 'congestion_r'})
        algo_df = algo_df.drop(['addr', 'tag', '여유있는', '재미있는', '친절한', 'activity_m', 'nature_m', 'fun_m', 'comfort_m', 'together_m', 'with_pet_s' ],1)

    # weights table
    def weights_table(self):
        weights_df = self.weights.rename(columns={'category' : 'cat',
                                  'origindf' : 'original_cat',
                                  'originalname' : 'tag',
                                  'colname' : 'tag_eng',
                                  'tagname' : 'sub_cat'
                                 })
        return weights_df
    
    # main_cat table
    def maincat_table(self):
        main_cat_df = self.main_cat.rename(columns={'contentId' : 'content_id',
                                    'camp' : 'place_name'})
        return main_cat_df
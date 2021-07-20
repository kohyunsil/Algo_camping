import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import sys
import os
sys.path.append(os.path.dirname(__file__))
import config as config

# 한글 폰트 설정
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
elif platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Linux':
    rc('font', family='NanumBarunGothic')
else:
    print('Unknown system... sorry~')

class CampMerge:

    def __init__(self):
        self.path = config.Config.PATH
        self.api_data = config.Config.API_DATA
        self.crawl_data = config.Config.CRAWL_DATA
        self.nv_data = config.Config.NV_DATA
        self.kk_data = config.Config.KK_DATA

    def camp_api_data_merge(self):
        camp_api_data = self.api_data
        camp_crawling_data = self.crawl_data
        datas = camp_crawling_data['link']
        data =[re.findall("\d+",data)[0] for data in datas]
        camp_crawling_data['url_num'] = data
        camp_crawling_data['url_num'] = camp_crawling_data['url_num'].astype('int')
        merge_file = pd.merge(camp_api_data, camp_crawling_data, how='left', left_on='contentId',  right_on='url_num')
        merge_file = merge_file.drop(['title', 'description', 'address', 'link', 'url_num'],1)

        data = merge_file.reset_index(drop=True)
        data['tags'] = data['tags'].str.replace(' ', '')
        data['tag'] = data.tags.str.replace('#', " ")
        data['tag'] = data['tag'].str.strip()
        data['tag'] = data['tag'].fillna('정보없음')

        out = []
        seen = set()
        for c in data['tag']:
            words = c.split()
            out.append(' '.join([w for w in words if w not in seen]))
            seen.update(words)
        data['unique_tag'] = out

        df = data[data['unique_tag'] != ""]
        df = df.reset_index(drop=True)

        df2 = df['unique_tag'].unique()
        df3 = " ".join(df2)
        df3 = df3.split(" ")

        def get_tag(i):
            dfs = data['tag'].str.contains(df3[i])
            data[df3[i]] = dfs.astype(int)

        for i in range(len(df3)):
            get_tag(i)

        tag_data = data.iloc[:, 90:]
        tag_data = tag_data.drop(['친절한', '재미있는', '여유있는'],1)
        camp_data1 = data[['facltNm', 'contentId', 'insrncAt', 'trsagntNo', 'mangeDivNm', 'manageNmpr', 'sitedStnc',
                           'glampInnerFclty',
                           'caravInnerFclty', 'trlerAcmpnyAt', 'caravAcmpnyAt', 'toiletCo', 'swrmCo', 'wtrplCo',
                           'brazierCl', 'sbrsCl',
                           'sbrsEtc', 'posblFcltyCl', 'extshrCo', 'frprvtWrppCo', 'frprvtSandCo', 'fireSensorCo',
                           'animalCmgCl']]
        camp_algo_merge = pd.concat([camp_data1, tag_data], 1)

        def col_count(colname):
            camp_algo_merge[f'{colname}'] = camp_algo_merge[f'{colname}'].str.count(',') + 1
            camp_algo_merge[f'{colname}'] = camp_algo_merge[f'{colname}'].fillna(0)
            camp_algo_merge[f'{colname}'] = camp_algo_merge[f'{colname}'].astype('int')

        for i in ['glampInnerFclty', 'caravInnerFclty', 'sbrsCl', 'sbrsEtc', 'posblFcltyCl']:
            col_count(i)

        camp_algo_merge = camp_algo_merge.rename(columns={'facltNm':'camp'})
        camp_algo_merge = camp_algo_merge.rename(
            columns={'사이트간격이넓은': '사이트 간격이 넓은', '온수잘나오는': '온수 잘 나오는', '차대기편한': '차대기 편한',
                     '아이들놀기좋은': '아이들 놀기 좋은', '자전거타기좋은': '자전거 타기 좋은', '별보기좋은': '별 보기 좋은',
                     '수영장있는': '수영장 있는', '물놀이하기좋은': '물놀이 하기 좋은', '그늘이많은': '그늘이 많은', '바다가보이는': '바다가 보이는'})

        # camp_algo_merge.to_csv('../datas/camp_algo_merge.csv', index=False, encoding='utf-8-sig')

        return camp_algo_merge


class ReviewPre(CampMerge):

    def review_preprocessing(self):
        """ 카카오 데이터는 네이버 카테고리 학습 후 반영"""

        nv_data = self.nv_data
        kk_data = self.kk_data


        # naver_review_data preprocessing
        nv_data['user_info'] = nv_data['user_info'].fillna(0)
        nv_data = nv_data[nv_data['user_info'] != 0]
        nv_data['user_info'] = nv_data['user_info'].apply(lambda x: x.split('\n')[-1])
        nv_data['visit_info'] = nv_data['visit_info'].apply(lambda x: x.split('번째')[0][-1])
        nv_data = nv_data[nv_data['star'] != 'star']

        nv_data['star'] = nv_data['star'].astype('float64')
        nv_data['user_info'] = nv_data['user_info'].astype('float64')
        nv_data['visit_info'] = nv_data['visit_info'].astype('float64')
        nv_data = nv_data.drop(['addr', 'base_addr', 'user_name', 'visit_info'], 1)
        nv_data = nv_data.rename(
            columns={'title': 'camp', 'highlight_review': 'review', 'star': 'point', 'user_info': 'avg_point'})

        nv_data = nv_data[['camp', 'review', 'point', 'category', 'avg_point']]
        nv_data['point'] = nv_data['point'].astype('float64')
        nv_data['avg_point'] = nv_data['avg_point'].astype('float64')

        reviews_df = pd.concat([nv_data, kk_data], 0)

        # 가중치 [ point / (point / avg_point) ] * 0.01 → RobustScaler 적용
        reviews_df['weights'] = reviews_df['point'] * (reviews_df['point'] / reviews_df['avg_point'])
        reviews_df = reviews_df.reset_index(drop=True)

        rb = RobustScaler()
        rb_df = rb.fit_transform(reviews_df[['weights']])
        rb_df = pd.DataFrame(rb_df)

        rb_df = rb_df.rename(columns={0: 'weights2'})
        rb_df['weights2'] = rb_df['weights2'] * 0.01

        re_df = pd.concat([reviews_df, rb_df], 1)

        # final_point: point * (1+weights) → MinMaxScaler 적용 후 *5 (0~5 사이의 값)

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

        return re_df4


class ReviewCamp(ReviewPre):

    def review_camp_merge(self):
        cm = CampMerge()
        api_data = cm.camp_api_data_merge()
        df = self.review_preprocessing()
        df = df[['camp', 'category', 'final_point']]
        df = pd.pivot_table(df, index='camp', columns='category')
        df = df.fillna(0)
        df = df.reset_index()
        review_result = pd.concat([df["camp"], df["final_point"]], 1)

        camp_name = ['느티나무 캠핑장', '늘푸른캠핑장', '두리캠핑장', '둥지캠핑장', '백운계곡캠핑장', '별빛야영장',
                     '별헤는 밤', '산여울캠핑장', '소풍캠핑장', '솔바람 캠핑장', '솔밭야영장', '솔밭캠핑장', '포시즌',
                     '포시즌 캠핑장']

        for i in camp_name:
            review_result = review_result.query(f'camp != "{i}"')

        merge_result = pd.merge(api_data, review_result, how='outer', left_on='camp', right_on='camp')

        result1 = merge_result.iloc[:, 44:].fillna(0)
        result2 = merge_result.iloc[:, :44]
        algo_result = pd.concat([result2, result1], 1)
        algo_result = algo_result.rename(columns={'사이트 간격이 넓은':'spacious_s', '깨끗한':'clean_s', '온수 잘 나오는':'hot_water_s',
        '차대기 편한':'parking_s', '아이들 놀기 좋은':'with_child_s', '생태교육':'ecological_s', '문화유적':'cultural_s', '축제':'festival_s',
        '둘레길':'trail_s', '자전거 타기 좋은':'bicycle_s', '별 보기 좋은':'star_s', '힐링':'healing_s', '커플':'with_couple_s', '가족':'with_family_s',
        '수영장 있는':'pool_s', '계곡옆':'valley_s', '물놀이 하기 좋은':'waterplay_s', '물맑은':'pure_water_s', '그늘이 많은':'shade_s',
        '바다가 보이는':'ocean_s', '익스트림':'extreme_s', '가격':'price_r', '만족도':'satisfied_r', '맛':'taste_r', '메인시설':'main_r','목적':'object_r',
        '부대/공용시설': 'facility_r', '분위기':'atmos_r', '비품':'equipment_r','서비스':'service_r', '수영장':'pool_r',
        '시설물관리':'manage_r', '아이 만족도':'childlike_r', '예약':'reservation_r', '와이파이':'wifi_r','위치':'location_r', '음식/조식':'food_r',
        '입장': 'enter_r', '전망':'view_r', '주차':'parking_r', '즐길거리': 'exciting_r', '청결도': 'clean_r', '편의/부대시설':'conv_facility_r', '혼잡도': 'congestion_r'})
        # algo_result.set_index('camp', inplace=True)


        # algo_result.to_csv('../datas/algo_merge_result.csv', encoding='utf-8-sig', index=False)

        return print(algo_result)
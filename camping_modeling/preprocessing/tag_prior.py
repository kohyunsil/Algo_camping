import re
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import camp_api_crawling_merge as cacm


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


class TagMerge:
    def camp_api_data_merge(self, apifile, crawl_file):
        camp_api_data = pd.read_csv(f"../datas/{apifile}.csv", encoding='utf-8-sig')
        camp_crawling_data = pd.read_csv(f"../datas/{crawl_file}.csv", encoding='utf-8-sig')
        datas = camp_crawling_data['link']
        data = [re.findall("\d+", data)[0] for data in datas]
        camp_crawling_data['url_num'] = data
        camp_crawling_data['url_num'] = camp_crawling_data['url_num'].astype('int')
        merge_file = pd.merge(camp_api_data, camp_crawling_data, how='left', left_on='contentId', right_on='url_num')
        merge_file = merge_file.drop(['title', 'description', 'address', 'link', 'url_num'], 1)
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
        camp_data1 = data[['facltNm', 'contentId']]
        camp_algo_merge = pd.concat([camp_data1, tag_data], 1)
        camp_algo_merge = camp_algo_merge.rename(columns={'facltNm': 'camp', '사이트간격이넓은': '사이트 간격이 넓은',
                                                          '온수잘나오는': '온수 잘 나오는', '차대기편한': '차대기 편한',
                                                          '아이들놀기좋은': '아이들 놀기 좋은', '자전거타기좋은': '자전거 타기 좋은',
                                                          '별보기좋은': '별 보기 좋은', '수영장있는': '수영장 있는', '물놀이하기좋은': '물놀이 하기 좋은',
                                                          '그늘이많은': '그늘이 많은', '바다가보이는': '바다가 보이는'})

        return camp_algo_merge

    def review_data(self):

        grm = cacm.ReviewPre()
        re_df = grm.review_preprocessing('v5_category_re', 'kakao_review_cat_revised')

        ## 태그별 우선순위를 위한 preprocessing
        tag_df = re_df.drop(['point', 'count', 'avg_point'], 1)
        mm = MinMaxScaler()
        mm_fit = mm.fit_transform(tag_df.iloc[:, 2:])
        tag_df['mm_point'] = mm_fit
        tag_df = tag_df.drop('final_point', 1)
        df = pd.pivot_table(tag_df, index='camp', columns='category')
        df = df.fillna(0)
        df = df.reset_index()
        tag_result = pd.concat([df["camp"], df["mm_point"]], 1)

        camp_name = ['느티나무 캠핑장', '늘푸른캠핑장', '두리캠핑장', '둥지캠핑장', '백운계곡캠핑장', '별빛야영장',
                     '별헤는 밤', '산여울캠핑장', '소풍캠핑장', '솔바람 캠핑장', '솔밭야영장', '솔밭캠핑장', '포시즌',
                     '포시즌 캠핑장']

        for i in camp_name:
            tag_result = tag_result.query(f'camp != "{i}"')

        return tag_result

    def tag_merge(self, filename):
        algo_df = pd.read_csv(f'../datas/{filename}.csv')
        algo_df = algo_df.iloc[:, 2:]
        datas = self.camp_api_data_merge('camp_api_info_210619', 'camp_crawl_links')
        review = self.review_data()
        merge_result = pd.merge(datas, review, how='left', left_on='camp', right_on='camp')
        merge_result = merge_result.fillna(0)
        merge_result = merge_result.drop(['만족도', '가격', '목적', '메뉴', '예약', '음식양', '입장', '혼잡도'], 1)
        merge_result = merge_result.rename(
            columns={'친절한': 'friendly_s', '재미있는': 'exciting_s', '여유있는': 'relax_s', '사이트 간격이 넓은': 'spacious_s',
                     '깨끗한': 'clean_s', '온수 잘 나오는': 'hot_water_s', '차대기 편한': 'parking_s', '아이들 놀기 좋은': 'with_child_s',
                     '생태교육': 'ecological_s', '문화유적': 'cultural_s', '축제': 'festival_s', '둘레길': 'trail_s',
                     '자전거 타기 좋은': 'bicycle_s',
                     '별 보기 좋은': 'star_s', '힐링': 'healing_s', '커플': 'with_couple_s', '가족': 'with_family_s',
                     '수영장 있는': 'pool_s',
                     '계곡옆': 'valley_s', '물놀이 하기 좋은': 'waterplay_s', '물맑은': 'pure_water_s', '그늘이 많은': 'shade_s',
                     '바다가 보이는': 'ocean_s',
                     '익스트림': 'extreme_s', '맛': 'taste_r', '메인시설': 'main_r', '부대/공용시설': 'facility_r', '분위기': 'atmos_r',
                     '비품': 'equipment_r',
                     '서비스': 'service_r', '수영장': 'pool_r', '시설물관리': 'manage_r', '아이 만족도': 'childlike_r',
                     '와이파이': 'wifi_r', '위치': 'location_r',
                     '음식/조식': 'food_r', '전망': 'view_r', '주차': 'parking_r', '즐길거리': 'exciting_r', '청결도': 'clean_r',
                     '편의/부대시설': 'conv_facility_r'})
        merge_result = pd.concat([merge_result, algo_df], 1)
        # merge_result.to_csv('tag_prior.csv', encodings='utf-8-sig', index=False)

        return print(merge_result)
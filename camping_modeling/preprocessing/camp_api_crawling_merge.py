import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler, MaxAbsScaler


class CampMerge:

    def camp_api_data_merge(self, apifile, crawl_file):
        camp_api_data = pd.read_csv(f"../datas/{apifile}.csv", encoding='utf-8-sig')
        camp_crawling_data = pd.read_csv(f"../datas/{crawl_file}.csv", encoding='utf-8-sig')
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
        camp_algo_merge.to_csv('../datas/camp_algo_merge.csv', index=False, encoding='utf-8-sig')



class GocampReviewMerge(CampMerge):

    def review_camp_merge(self, api_data, naver_review_file, kakao_review_file):
        """ 카카오 데이터는 네이버 카테고리 학습 후 반영"""

        path = "../datas/"
        api_data = pd.read_csv(path + f'{api_data}.csv')
        nv_data = pd.read_csv(path + f'{naver_review_file}.csv')
        kk_data = pd.read_csv(path + f'{kakao_review_file}.csv', index_col=0)


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

        df = re_df4[['camp', 'category', 'final_point']]
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

        algo_result.to_csv('algo_merge_result.csv', encoding='utf-8-sig', index=False)



if __name__  == '__main__':
    c = CampMerge()
    grm = GocampReviewMerge()
    # c.camp_api_data_merge('camp_api_info_210619', 'camp_crawl_links')
    grm.review_camp_merge('camp_algo_merge', 'v5_category_re', 'kakao_review_cat_revised')

import algo_config as config
from tqdm import tqdm
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import camp_api_crawling_merge as cacm
import camping_server2.apis.gocamping_api as ga
import warnings

gocamping = ga.GocampingApi()
warnings.simplefilter("ignore")
TODAY = datetime.today().strftime('%m%d')


class TagMerge:
    def __init__(self):
        self.path = config.Config.PATH
        self.api_data = gocamping.gocampingAPI()
        self.crawl_data = config.Config.CRAWL_DATA
        self.dm = config.Config.DIMENSION

    def camp_data_merge(self):
        tags = cacm.CampMerge()
        camp_data1 = self.api_data[['facltNm', 'contentId']]
        camp_data_merge = pd.concat([camp_data1, tags.camp_api_preprocessing()], 1)
        camp_data_merge = camp_data_merge.rename(columns={'facltNm': 'camp'})

        return camp_data_merge

    def review_data(self):

        re_df = cacm.ReviewPre().review_preprocessing()

        # 태그별 우선순위를 위한 preprocessing
        tag_df = re_df.drop(['point', 'count', 'Unnamed: 0','avg_point'], 1)
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

    def tag_merge(self):
        algo_df = config.Config.ALGO_DF_FINAL
        algo_df = algo_df[['comfort', 'together', 'fun', 'healing', 'clean']].reset_index(drop=True)
        datas = self.camp_data_merge()
        review = self.review_data()
        merge_result = pd.merge(datas, review, how='left', left_on='camp', right_on='camp')
        merge_result = merge_result.fillna(0)
        merge_result = merge_result.drop(['만족도', '가격', '목적', '메뉴', '예약', '음식양', '입장', '혼잡도'], 1)
        re_cols = merge_result.columns.tolist()[2:]
        for re_col in re_cols:
            col_names = self.dm[self.dm.colname_kor == f'{re_col}']
            col_name = np.unique(col_names.colname)
            merge_result = merge_result.rename(columns = {f'{re_col}': f'{"".join(col_name)}'})

        merge_result = pd.concat([merge_result, algo_df], 1)
        #merge_result.to_csv(self.path + 'tag_merge.csv', encoding='utf-8-sig', index=False )
        return merge_result


class TagPoints:
    def __init__(self):
        self.path = config.Config.PATH
        self.df = TagMerge().tag_merge()
        self.df.set_index(['contentId'], drop=False, inplace=True)
        self.dm = config.Config.TAG_DM

    def get_tag_dict(self):
        df = self.dm
        tag_dict = {}
        for tagname in np.unique(df['tagname']):
            tag_list = df[df['tagname'] == tagname]['colname'].tolist()
            tag_dict[tagname] = tag_list
        return tag_dict

    def get_cat_num(self, tag_ls, content_id):
        df = self.dm
        cat_points = []
        for t in tag_ls:
            cat = df[df['tagname'] == t]['category'].iloc[0]
            cat_point = float(self.df[self.df['contentId'] == content_id][cat.lower()])
            cat_points.append(cat_point)
        return cat_points

    def make_tag_df(self, content_id=False):
        self.df.replace(0, np.NaN, inplace=True)
        tag_dict = self.get_tag_dict()
        tag_point_df = pd.DataFrame(self.df['camp'])

        for tagname in np.unique(self.dm['tagname']):
            if not content_id:
                for idx in self.df.index:
                    tag_point_df[tagname] = np.mean(self.df[tag_dict[tagname]].loc[idx])
            if content_id:
                tag_point_df = tag_point_df.loc[[content_id]]
                tag_point_df[tagname] = np.mean(self.df[tag_dict[tagname]].loc[content_id])

        return tag_point_df

    def apply_cat_points(self, content_id):
        tag_point_df = self.make_tag_df(content_id=content_id)
        tag_point_df.drop('camp', axis=1, inplace=True)
        target_df = tag_point_df.loc[[content_id]].T.sort_values(content_id, ascending=False)
        target_df['cat_points'] = self.get_cat_num(target_df.index.tolist(), content_id)
        # target_df['total_points'] = target_df[content_id] * target_df['cat_points']
        target_df['total_points'] = target_df[content_id] * 100 + target_df['cat_points'] / 100  # 태그 크기 차등을 위해 지정
        target_df = target_df.sort_values('total_points', ascending=False)
        return target_df

    def tag_priority(self, content_id, rank=5):
        target_df = self.apply_cat_points(content_id)
        target_df.dropna(axis=0, inplace=True)

        target_df = target_df.sort_values('total_points', ascending=False)
        tag_prior_ls = target_df.iloc[:rank].index.tolist()
        tag_point_ls = target_df.iloc[:rank]['total_points'].tolist()

        print(content_id, tag_prior_ls, tag_point_ls)
        return tag_prior_ls, tag_point_ls

    def make_tag_prior_df(self, rank=5):
        tag_dict, point_dict = {}, {}
        for content_id in tqdm(self.df.index.tolist()):
            tag_ls, point_ls = self.tag_priority(content_id=content_id, rank=rank)
            tag_dict[content_id] = tag_ls
            point_dict[content_id] = point_ls

        tag_df = pd.DataFrame(list(tag_dict.items()), columns=['contentId', '5tags'])
        point_df = pd.DataFrame(list(point_dict.items()), columns=['contentId', '5points'])
        tag_point_df = pd.merge(tag_df, point_df, on='contentId')

        # for n in range(1, 6):
        #     tag_point_df[f'tag{n}'] = ""
        #     tag_point_df[f'tag_point{n}'] = ""
        #
        # for row, tag in enumerate(tag_point_df['5tags'].tolist()):
        #     for idx in range(len(tag)):
        #         try:
        #             tag_point_df[f'tag{idx + 1}'].iloc[row] = tag_point_df['5tags'][row][idx]
        #         except:
        #             tag_point_df[f'tag{idx + 1}'].iloc[row] = np.nan
        #
        # for row, point in enumerate(tag_point_df['5points'].tolist()):
        #     for idx in range(len(point)):
        #         try:
        #             tag_point_df[f'tag_point{idx + 1}'].iloc[row] = float(tag_point_df['5points'][row][idx])
        #         except:
        #             tag_point_df[f'tag_point{idx + 1}'].iloc[row] = np.nan
        # tag_point_df[['tag_point1', 'tag_point2', 'tag_point3', 'tag_point4', 'tag_point5']] = \
        #     tag_point_df[['tag_point1', 'tag_point2', 'tag_point3', 'tag_point4', 'tag_point5']].apply(pd.to_numeric)
        # tag_point_df.drop(['5tags', '5points'], axis=1, inplace=True)
        # tag_point_df.to_csv(self.path + f"top{rank}_tags_{config.Config.NOW}.csv")
        print(tag_point_df)
        return tag_point_df

import pandas as pd
import numpy as np
import warnings
from app.config import Config

warnings.simplefilter("ignore")


class TagPoints:
    def __init__(self):
        self.df = Config.TAG_DF
        self.dm = Config.TAG_DM

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
        self.df.set_index(['contentId'], drop=False, inplace=True)
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
        target_df['total_points'] = target_df[content_id] * target_df['cat_points']
        target_df = target_df.sort_values('total_points', ascending=False)
        return target_df

    def tag_priority(self, content_id, rank=5):
        try:
            target_df = self.apply_cat_points(content_id)
            target_df.dropna(axis=0, inplace=True)
            uq_points = np.unique(target_df[content_id].iloc[:rank]).tolist()
            uq_points.sort(reverse=True)
            uq_tag_len = len(uq_points)

            # 동점자가 있다면 원래 포인트 cat_points 반영된 point 로 정렬 후 상위 rank 개
            if uq_tag_len < rank:
                tag_prior_ls = []
                for p in uq_points:
                    temp_df = target_df[target_df[content_id] == p].sort_values('total_points', ascending=False)
                    for t in temp_df.index:
                        tag_prior_ls.append(t)
                tag_prior_ls = tag_prior_ls[:rank]

            # 동점자가 없다면 원래 포인트 상위 rank 개
            else:
                target_df = target_df.sort_values(content_id, ascending=False)
                tag_prior_ls = target_df.iloc[:rank].index.tolist()
        except:
            # content_id에 대한 별점, 점수 산출 불가인 경우
            return []

        return tag_prior_ls

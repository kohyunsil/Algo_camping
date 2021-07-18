import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
import config as config

warnings.simplefilter("ignore")


class TagPoints:
    def __init__(self):
        self.path = config.Config.PATH
        self.df = config.Config.TAG_DF
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
        self.df.set_index(['contentId'], drop=False, inplace=True)
        self.df.replace(0, np.NaN, inplace=True)
        tag_dict = self.get_tag_dict()
        tag_point_df = pd.DataFrame(self.df['camp'])

        for tagname in tqdm(np.unique(self.dm['tagname'])):
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
        target_df = self.apply_cat_points(content_id)
        tag_len = len(np.unique(target_df[content_id].iloc[:rank].tolist()))
        # 동점자가 없다면 원래 포인트 상위 rank 개
        if tag_len == rank:
            target_df = target_df.sort_values(content_id, ascending=False)
        # 동점자가 있다면 원래 포인트 cat_points 반영된 point 로 정렬 후 상위 rank 개
        elif tag_len < rank:
            target_df = target_df.sort_values('total_points', ascending=False)
        #
        # elif tag_len < rank:
        #     target_df = target_df.sort_values('')
        #     target_df =


        tag_prior_ls = target_df.iloc[:rank].index.tolist()
        print(tag_prior_ls)
        return tag_prior_ls


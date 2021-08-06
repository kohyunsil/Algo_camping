import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from konlpy.tag import Okt
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import hdbscan
from sklearn.manifold import TSNE
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

import nlp_clustering as nc
import algostar.config as config
import algostar.algo_points as ap


class CampCluster(nc.NlpCluster):
    def __init__(self):
        self.path = config.Config.PATH
        # ag = ap.AlgoPoints()
        nlp = nc.NlpCluster()
        # algo_df = ag.make_algo_df(just_load_file="0719")
        algo_df = config.Config.TAG_DF
        self.algo_df = algo_df.loc[:, ~algo_df.columns.str.match("Unnamed")]
        # self.nlp_df = pd.read_csv(self.path + "camp_description.csv")[['facltNm', 'labels']]
        nlp_df = nlp.nlp_clustering(vec='tfidf', min_cluster_size=30)[['contentId', 'cluster']]
        self.nlp_df = nlp_df.astype('int')
        self.nlp_df.drop_duplicates('contentId', keep=False, inplace=True)

    def preprocessing(self, over_avg=False):
        """over_avg = True 일 경우, cat_points의 합계가 mean 이상인 약 상위 50%의 캠핑장만 대상으로 함 """
        merge_df = pd.merge(self.algo_df, self.nlp_df, how="left", left_on="contentId", right_on="contentId")
        merge_df["cluster"] = [str(int(r)) if np.isnan(r) == False else r for r in merge_df["cluster"]]
        merge_df = pd.get_dummies(merge_df, columns=['cluster'], dummy_na=True)
        merge_df.set_index(['camp', 'contentId'], inplace=True)
        if over_avg:
            merge_df['total'] = merge_df[['comfort', 'together', 'fun', 'healing', 'clean']].sum(axis=1)
            merge_df = merge_df[merge_df['total'] >= merge_df['total'].mean()]
            merge_df.drop('total', axis=1, inplace=True)
        else:
            pass
        return merge_df

    def hdbscan_clustering(self, target_data='camp', min_cluster_size=5, over_avg=False):
        if target_data == 'camp':
            fit_data = self.tsne_dm_reduction('camp', over_avg)
        else:
            fit_data = target_data

        # 모델 객체 생성
        clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=1, gen_min_span_tree=True,
                                    prediction_data=True)
        clusterer.fit(fit_data)
        # 예측 데이터 생성
        pred_hds = clusterer.fit_predict(fit_data)
        # 데이터 프레임 만들기
        df = self.preprocessing(over_avg)
        df["cluster"] = pred_hds
        df["x"] = fit_data['x'].tolist()
        df["y"] = fit_data['y'].tolist()
        print(f"Cluster 개수: {len(np.unique(df['cluster']))} 개")
        print(f"original data length: {len(df)} / clustering data length: {len(pred_hds)}")
        print(df.groupby('cluster')['cluster'].count())
        print("Condensed tree plot")
        clusterer.condensed_tree_.plot(select_clusters=True)  # , selection_palette=sns.color_palette())
        plt.show()
        self.draw_scatter(df)
        return df

    def cluster_eda(self, df):
        columns = ['comfort', 'together', 'fun', 'healing', 'clean', 'x']
        pv1 = pd.pivot_table(df, index='cluster',
                             aggfunc={'comfort': 'mean', 'together': 'mean', 'fun': 'mean',
                                      'healing': 'mean', 'clean': 'mean', 'x': 'count'})[columns]
        pv2 = pv1[1:]
        print("Dataframe Describe")
        print(pd.DataFrame(pv2.describe()))
        # 클러스터 간 편차 탐색 boxplot
        sns.set(font_scale=2.5)
        fig, ax = plt.subplots(1, 2, figsize=(40, 15))
        sns.boxplot(data=pv1[columns[:-1]], ax=ax[0])
        sns.boxplot(data=pv2[columns[:-1]], ax=ax[1])
        ax[0].set_title("Category boxplot")
        ax[1].set_title("Category boxplot without outlier")
        fig.show()

        # 클러스터별 특성 탐색 boxplot
        df2 = df[['cluster', 'comfort', 'together', 'fun', 'healing', 'clean']].copy()
        df2.set_index('cluster', drop=True, inplace=True)
        sns.set(font_scale=1.5)
        c_ls = np.unique(df2.index).tolist()
        fig, ax = plt.subplots(len(c_ls), 1, sharey=True, figsize=(30, 80))
        for idx, c in enumerate(c_ls):
            t_df = df2[df2.index == c]
            sns.boxplot(data=t_df, ax=ax[idx])
            ax[idx].set_title(f"Cluster {c}")
        fig.show()

        return pv1

    def export_result(self, df):
        path = "results/"
        df.to_csv(path + f"clustering_result_{config.Config.NOW}.csv", encoding='utf-8-sig')
        print("Report has Saved!")

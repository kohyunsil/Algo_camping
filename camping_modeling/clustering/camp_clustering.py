import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import hdbscan
from sklearn.manifold import TSNE
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import algostar.config as config
import algostar.calc_logic as cl
import algostar.algo_points as ap


class CampCluster:
    def __init__(self):
        self.path = config.Config.PATH
        ag = ap.AlgoPoints()
        algo_df = ag.make_algo_df(just_load_file="max")
        self.algo_df = algo_df.loc[:, ~algo_df.columns.str.match("Unnamed")]
        self.nlp_df = pd.read_csv(self.path + "camp_description.csv")[['facltNm', 'labels']]
        self.nlp_df.drop_duplicates('facltNm', keep=False, inplace=True)

    def preprocessing(self):
        merge_df = pd.merge(self.algo_df, self.nlp_df, how="left", left_on="camp", right_on="facltNm")
        merge_df.drop('facltNm', axis=1, inplace=True)
        merge_df["labels"] = [str(int(r)) if np.isnan(r) == False else r for r in merge_df["labels"]]
        merge_df = pd.get_dummies(merge_df, columns=['labels'], dummy_na=True)
        merge_df.set_index(['camp', 'contentId'], inplace=True)
        return merge_df

    def tsne_dm_reduction(self):
        tsne = TSNE()
        df = self.preprocessing()
        tsne_fit = tsne.fit_transform(df)
        tsne_df = pd.DataFrame(tsne_fit, index=df.index, columns=['x', 'y'])
        return tsne_df

    def hdbscan_clustering(self, min_cluster_size=5, tsne=True):
        # 차원 축소 여부 결정
        if tsne:
            fit_data = self.tsne_dm_reduction()
        else:
            fit_data = self.preprocessing()

        # 모델 객체 생성
        clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=1, gen_min_span_tree=True,
                                    prediction_data=True)
        clusterer.fit(fit_data)
        # 예측 데이터 생성
        pred_hds = clusterer.fit_predict(fit_data)
        # 데이터 프레임 만들기
        df = self.algo_df.copy()
        df["cluster"] = pred_hds
        df["x"] = fit_data['x'].tolist()
        df["y"] = fit_data['y'].tolist()
        print(f"Cluster labels: {len(np.unique(df['cluster']))} 개")
        print(f"original data length: {len(self.algo_df)} / clustering data length: {len(pred_hds)}")
        # print("아웃라이어 스코어: ", clusterer.outlier_scores_)
        print(df.groupby('cluster')['contentId'].count())
        print("Condensed tree plot")
        clusterer.condensed_tree_.plot(select_clusters=True) #, selection_palette=sns.color_palette())
        plt.show()
        self.draw_scatter(df)
        return df

    def draw_scatter(self, df):
        df2 = df.copy()
        df2.drop(df[df['cluster'] == -1].index, inplace=True)
        fig, ax = plt.subplots(2, 1, figsize=(40, 40))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        ax1.scatter(df['x'], df['y'], c=df["cluster"], s=300, cmap="tab20", alpha=0.6)
        ax1.set_title("HDBSCAN", fontsize=30)
        ax2.scatter(df2['x'], df2['y'], c=df2["cluster"], s=300, cmap="tab20", alpha=0.6)
        ax2.set_title("HDBSCAN without Outlier", fontsize=30)
        fig.show()

    def cluster_eda(self, df):
        columns = ['comfort', 'together', 'fun', 'healing', 'clean', 'x']
        pv1 = pd.pivot_table(df, index='cluster',
                             aggfunc={'comfort': 'mean', 'together': 'mean', 'fun': 'mean',
                                      'healing': 'mean', 'clean': 'mean', 'x': 'count'})[columns]
        pv2 = pv1[1:]
        print("Dataframe Describe")
        print(pd.DataFrame(pv2.describe()))
        # draw boxplot
        sns.set(font_scale=2.5)
        fig, ax = plt.subplots(1, 2, figsize=(40, 15))
        sns.boxplot(data=pv1[columns[:-1]], ax=ax[0])
        sns.boxplot(data=pv2[columns[:-1]], ax=ax[1])
        ax[0].set_title("Category boxplot")
        ax[1].set_title("Category boxplot without outlier")
        fig.show()

        return pv1

    def export_result(self, df):
        path = "./results/"
        df.to_csv(path+f"clustering_result_{config.Config.NOW}.csv")
        print("Report has Saved!")

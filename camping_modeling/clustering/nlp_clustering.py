import algostar.config as config
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import hdbscan
from sklearn.manifold import TSNE
from urllib.request import Request, urlopen
import xmltodict
import json
from pandas.io.json import json_normalize
import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))


class NlpCluster():
    def __init__(self):
        self.path = config.Config.PATH
        self.secretKey = config.Config.PUBLIC_API_KEY

    def gocampingAPI(self):
        url = 'http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?'
        param = 'ServiceKey=' + self.secretKey + '&MobileOS=ETC&MobileApp=AppTest&numOfRows=3000'

        request = Request(url + param)
        request.get_method = lambda: 'GET'
        response = urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            responseData = response.read()
            rD = xmltodict.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)

            camp_api_df = json_normalize(rDD['response']['body']['items']['item'])
            print(camp_api_df.head())
            return camp_api_df
        else:
            print("API No response")

    def make_camp_nlp_data(self):
        camp_api_df = self.gocampingAPI()
        camp_nlp_df = camp_api_df[['contentId', 'facltNm', 'lineIntro']].copy() #, 'intro'
        camp_nlp_df.dropna(thresh=3, axis=0, inplace=True)
        camp_nlp_df.reset_index(drop=True, inplace=True)
        camp_nlp_df["full_text"] = camp_nlp_df["lineIntro"]  #.map(str) + " " + camp_nlp_df["intro"].map(str)
        camp_nlp_df.drop(['lineIntro'], axis=1, inplace=True)  #, 'intro'
        print(camp_nlp_df.head())
        return camp_nlp_df

    def nlp_cleansing(self):
        data = self.make_camp_nlp_data()
        okt = Okt()
        full_text = data["full_text"]
        result_list = []
        english = re.compile(r'[a-zA-Z]')

        for i in tqdm(range(len(full_text))):
            rv = str(full_text[i])

            if len(rv) > 1:
                rv = re.sub(english, "", rv)
                a = re.sub(' ', 's', rv)  # 띄어쓰기 위해 s 붙힘
                b = okt.pos(a, stem=True, norm=True)
                string = ''
                for word in b:  # tokenize str version
                    string += word[0]
                c = re.sub('s', ' ', string)  # 띄어쓰기 분리
                result_list.append(c)
            else:
                result_list.append("")
        data["full_text"] = result_list
        print(data["full_text"][:10])
        print(f"---- Cleansing Succeed! ----")
        return data

    def doc2vec(self):
        o_data = self.nlp_cleansing()
        # o_data = pd.read_csv("../../datas/nlp_cleansed_data.csv", encoding="utf-8-sig")
        data = o_data["full_text"]
        tagged_data = []
        for i, _d in enumerate(data):
            tagged_data.append(TaggedDocument(words=word_tokenize(_d.lower()), tags=[o_data['facltNm'].iloc[i]]))

        max_epochs, vec_size, alpha = 3, 100, 0.025
        model = Doc2Vec(vector_size=vec_size,
                        alpha=alpha,
                        min_alpha=0.00025,
                        min_count=1,
                        dm=1)

        model.build_vocab(tagged_data)

        for epoch in range(max_epochs):
            print('iteration {0}'.format(epoch))
            model.train(tagged_data,
                        total_examples=model.corpus_count,
                        epochs=model.epochs)
            # decrease the learning rate
            model.alpha -= 0.0002
            # fix the learning rate, no decay
            model.min_alpha = model.alpha

        d2v = model.docvecs.vectors_docs  # document vector 전체를 가져옴
        print(d2v)
        return d2v, o_data

    def tfidf_vec(self):
        o_data = self.nlp_cleansing()
        # o_data = pd.read_csv("../../datas/nlp_cleansed_data.csv", encoding="utf-8-sig")
        data = o_data["full_text"]
        tfidf_vectorizer = TfidfVectorizer(min_df=5, ngram_range=(1, 5))
        tfidf_vectorizer.fit(data)
        tfv = tfidf_vectorizer.transform(data).toarray()
        print(tfv)
        return tfv, o_data

    def tsne_dm_reduction(self, data='camp', over_avg=False):
        tsne = TSNE()
        if data == 'camp':
            df = self.preprocessing(over_avg)
        else:
            df = data
        tsne_fit = tsne.fit_transform(df)
        try:
            tsne_df = pd.DataFrame(tsne_fit, index=df.index, columns=['x', 'y'])
        except:
            tsne_df = pd.DataFrame(tsne_fit, columns=['x', 'y'])
        return tsne_df

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
        return fig

    def nlp_clustering(self, vec='tfidf', min_cluster_size=30):
        if vec == 'd2v':
            vector, o_data = self.doc2vec()
        elif vec == 'tfidf':
            vector, o_data = self.tfidf_vec()
        else:
            print("Only vec='d2v' or vec='tfidf' is available.")
            pass
        tsne_df = self.tsne_dm_reduction(data=vector)
        tsne_df.set_index(o_data["contentId"], inplace=True)
        print(tsne_df.head())
        clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=1, gen_min_span_tree=True,
                                    prediction_data=True)
        clusterer.fit(tsne_df)
        # 예측 데이터 생성
        pred_hds = clusterer.fit_predict(tsne_df)
        # 데이터 프레임 만들기
        df = o_data
        df["cluster"] = pred_hds
        df["x"] = tsne_df['x'].tolist()
        df["y"] = tsne_df['y'].tolist()
        print(f"Cluster labels: {len(np.unique(df['cluster']))} 개")
        print(f"original data length: {len(df)} / clustering data length: {len(pred_hds)}")
        # print("아웃라이어 스코어: ", clusterer.outlier_scores_)
        print(df.groupby('cluster')['cluster'].count())
        print("Condensed tree plot")
        clusterer.condensed_tree_.plot(select_clusters=True)  # , selection_palette=sns.color_palette())
        plt.show()
        self.draw_scatter(df)
        return df

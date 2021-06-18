import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 설정
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

import nltk
from konlpy.tag import *
from konlpy.utils import pprint
from konlpy.tag import Okt
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
# import sklearn.cluster.KMeans as km

class Review_nlp:
    def __init__(self):
        self.kakao = pd.read_csv("../../datas/kakao_camping_review_revised.csv", encoding='utf-8-sig')

    def read_file(self, filename):
        path = "../../datas/"
        data = pd.read_csv(path+f"{filename}.csv", encoding='utf-8-sig')
        return data

    def rv_tokenizing(self, filename, colname):
        data = self.read_file(filename)
        okt = Okt()
        reviews = data[f"{colname}"]
        result_list = []
        english = re.compile(r'[a-zA-Z]')

        for i in range(len(reviews)):
            rv = str(reviews[i])

            if len(rv) > 0:
                rv = re.sub(english,"",rv)
                b = okt.pos(rv, stem = True, norm= True)  # tokenize
                sentence = []
                for word in b:
                    sentence.append(word[0])
                result_list.append(sentence)
            else:
                result_list.append("")
        data['contents'] = result_list
        return data

    def vectorizing(self):
        data = self.rv_tokenizing(filename, colname)
        reviews = data['contents']
        model = Word2Vec(reviews, sg=1, # skinp-gram: 중심단어로 주변단어 예측
                         window=5,      # 중심 단어로부터 좌우 5개까지 학습에 적용
                         min_count=10)   # 전체 문서에서 최소 10회 이상 출현 단어로 학습
        model.save('../models/model.model')
        # word_vectors = model.wv
        # word_vectors.save('../models/word_vectors.kv')

    def load_model(self):
        word_vectors = KeyedVectors.load('../models/word_vectors.kv')

        # print(list(word_vectors.index_to_key))
        # vocabs = list(word_vectors.index_to_key)
        # word_vectors_list = [word_vectors[v] for v in vocabs]
        #
        # pca = PCA(n_components=2)
        # xys = pca.fit_transform(word_vectors_list)
        # xs = xys[:, 0]
        # ys = xys[:, 1]
        #
        # plt.figure(figsize=(8, 6))
        # plt.title("try 1")
        # plt.scatter(xs, ys, marker='o')
        # for i, v in enumerate(vocabs):
        #     plt.annotate(v, xy=(xs[i], ys[i]))
        # plt.show()

        model = Word2Vec.load("../models/model.model")
        pretrained_model = KeyedVectors.load_word2vec_format("../models/ko.bin", binary=True)
        model.intersect_word2vec_format("../models/ko.bin", binary=True)
        word_vectors = model.wv
        vocabs = list(word_vectors.index_to_key)
        word_vectors_list = [word_vectors[v] for v in vocabs]

        pca = PCA(n_components=2)
        xys = pca.fit_transform(word_vectors_list)
        xs = xys[:, 0]
        ys = xys[:, 1]

        plt.figure(figsize=(8, 6))
        plt.title("try 2")
        plt.scatter(xs, ys, marker='o')
        for i, v in enumerate(vocabs):
            plt.annotate(v, xy=(xs[i], ys[i]))
        plt.show()
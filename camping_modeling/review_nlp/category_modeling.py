import numpy as np
import pandas as pd
import pickle
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

import kakao_review_nlp as nlp

class CategoryModel:
    def __init__(self):
        pass

    def make_cat_predictor(self):
        # get tokenized data
        s = nlp.Review_nlp()
        o_data = s.rv_tokenizing('v5_category_re', 'highlight_review')
        data = o_data[['highlight_review', 'category']]
        data.dropna(axis=0, inplace=True)

        train_x, test_x, train_y, test_y = train_test_split(
            data.highlight_review, data.category, test_size=0.2, random_state=0,
            stratify=data.category
        )

        # 모델 학습
        clf = Pipeline([
            ('vect', CountVectorizer()),
            ('tfdif', TfidfTransformer()),
            ('clf', svm.LinearSVC(C=0.4)),
            # ('clf', MultinomialNB(alpha=0.01)),
        ])
        model = clf.fit(train_x, train_y)
        print("모델 정확도: ", np.round(model.score(test_x, test_y), 4) * 100)

        with open("../models/model2.pkl", "wb") as file:
            pickle.dump(model, file)
        print("Model saved!")

    def apply_cat_predictor(self):
        with open("../models/model2.pkl", "rb") as file:
            load_model = pickle.load(file)

        kakao = pd.read_csv("../../datas/kakao_camping_review_revised.csv", encoding='utf-8-sig')
        cat_list = []
        for k in kakao['contents']:
            try:
                result = load_model.predict([k])[0]
            except:
                result = ""
            cat_list.append(result)
        kakao['category'] = cat_list
        kakao.to_csv("../../datas/kakao_review_cat_predict.csv", encoding='utf-8-sig')
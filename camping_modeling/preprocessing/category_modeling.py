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

    def make_cat_predictor(self, dataname, colname, labelname):
        # get tokenized data
        s = nlp.Review_nlp()
        o_data = s.rv_tokenizing(dataname, colname)
        # o_data = s.read_file("review_hdbscan")
        print("Data loaded")
        data = o_data[[f'{colname}', f'{labelname}']]
        data.dropna(axis=0, inplace=True)

        train_x, test_x, train_y, test_y = train_test_split(
            data[f'{colname}'], data[f'{labelname}'], test_size=0.2, random_state=0,
            stratify=data[f'{labelname}']
        )

        # 모델 학습
        print("Model learning started")
        clf = Pipeline([
            ('vect', CountVectorizer()),
            ('tfdif', TfidfTransformer()),
            ('clf', svm.LinearSVC(C=0.4)),
            # ('clf', MultinomialNB(alpha=0.01)),
        ])
        model = clf.fit(train_x, train_y)
        print("모델 정확도: ", np.round(model.score(test_x, test_y), 4) * 100)

        with open(f"../models/{dataname}_cls.pkl", "wb") as file:
            pickle.dump(model, file)
        print("Model saved!")

    def apply_cat_predictor(self, modelname, newfile, colname):
        with open(f"../models/{modelname}.pkl", "rb") as file:
            load_model = pickle.load(file)

        newfile = pd.read_csv(f"../../datas/{newfile}.csv", encoding='utf-8-sig')
        cat_list = []
        for k in newfile[f'{colname}']:
            try:
                result = load_model.predict([k])[0]
            except:
                result = ""
            cat_list.append(result)
        newfile['category'] = cat_list
        newfile.to_csv(f"../../datas/{modelname}_cat_predict.csv", encoding='utf-8-sig')
import numpy as np
import pandas as pd
import pickle
from tqdm import tqdm
import re
import kss
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from sklearn.pipeline import Pipeline
import warnings
import config as config
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


class CategoryModel:
    def __init__(self):
        self.path = config.Config.PATH
        self.kk_data = config.Config.KK_DATA
        self.nv_data = config.Config.NV_DATA

    def rv_cleansing(self, target_col, filename):
        if filename == 'nv':
            data = self.nv_data
        elif filename == 'kk':
            data = self.kk_data
        else:
            data = pd.read_csv(self.path+f"{filename}.csv", encoding='utf-8-sig', low_memory=False)

        okt = Okt()
        reviews = data[f"{target_col}"]
        result_list = []
        english = re.compile(r'[a-zA-Z]')

        for i in tqdm(range(len(reviews))):
            rv = str(reviews[i])

            if len(rv) > 0:
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
        data[f"{target_col}"] = result_list
        print(data[f"{target_col}"][:10])
        print(f"---- {filename} cleansing succeed! ----")
        return data

    def kk_sent_sep(self):
        kk = self.rv_cleansing('contents', 'kk')
        kk = kk[['contents', 'place_name', 'point']]  # , 'username', 'date']]
        camp_star = kk.groupby('place_name').mean().round(3)

        # 후기 없이 별점만 있는 데이터 drop
        kk.drop(kk[kk['contents'].isnull() == True].index, axis=0, inplace=True)
        kk['contents'] = [r.replace("/n", ". ") for r in kk['contents']]
        kk['contents'] = [re.sub(r"[^가-힣0-9.,'?!]", " ", r) for r in kk['contents']]
        # 문장별 분리
        kk['contents_sent'] = [kss.split_sentences(r) for r in kk['contents']]
        kk = kk.reset_index(drop=True)

        sep_sent_list, place_name_list, point_list, date_list = [], [], [], []

        for idx, cs in enumerate(kk['contents_sent']):
            for sent in cs:
                sep_sent_list.append(sent)
                place_name_list.append(kk['place_name'].iloc[idx])
                point_list.append(kk['point'].iloc[idx])

        kk_sent = pd.DataFrame({'review': sep_sent_list,
                                'camp': place_name_list,
                                'point': point_list})
        kk_sent['avg_point'] = [camp_star['point'][name] for name in kk_sent['camp']]

        return kk_sent

    def make_cat_predictor(self, target_col, label_name):
        # get tokenized data
        o_data = self.rv_cleansing(target_col, 'nv')
        print("Data loaded")
        data = o_data[[f'{target_col}', f'{label_name}']].copy()
        data.dropna(axis=0, inplace=True)

        train_x, test_x, train_y, test_y = train_test_split(
            data[f'{target_col}'], data[f'{label_name}'], test_size=0.2, random_state=0,
            stratify=data[f'{label_name}'])

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

        with open(f"../models/rv_cat_cls.pkl", "wb") as file:
            pickle.dump(model, file)
        print("Model saved!")
        return model

    def kk_apply_cat_predictor(self, target_col, make_cat_predictor=False):
        """ make_cat_predictor=False
            : 기존에 저장되어있는 네이버 카테고리 분류기 rv_cat_cls.pkl 를 불러와서 예측
            make_cat_predictor=True
            : 새롭게 네이버 카테고리 분류기 rv_cat_cls.pkl 를 만든 후 불러와서 예측 (약 15분 소요)"""
        kk_cat = self.kk_sent_sep()

        if make_cat_predictor is False:
            with open(f"../models/rv_cat_cls.pkl", "rb") as file:
                load_model = pickle.load(file)
        else:
            load_model = self.make_cat_predictor('highlight_review', 'category')
        print("Model loaded")

        cat_list = []
        for k in kk_cat[f'{target_col}']:
            try:
                result = load_model.predict([k])[0]
            except:
                result = ""
            cat_list.append(result)
        kk_cat['category'] = cat_list

        kk_cat.to_csv(f"{self.path}kk_cat_predict_{config.Config.NOW}.csv", encoding='utf-8-sig')
        return kk_cat

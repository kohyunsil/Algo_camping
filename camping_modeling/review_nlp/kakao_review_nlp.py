import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from konlpy.tag import *
from konlpy.utils import pprint

class review_nlp:
    def __init__(self):
        self.kakao = pd.read_csv("../../datas/kakao_camping_review_revised.csv", encoding='utf-8-sig')
        self.po_dict = ['좋','친절','괜찮','최고','빠르','짱','훌륭','추천','감사','구수','최상','대박','훈훈','특별','개이득',
                        '최고','만족','세련','최고','감동','친절','스윗','센스','괜찮','착하다','저렴','적당','싸다','좋다','합리적',
                        '훌륭','백프','만족','마음','든든','알맞다','무난','괜춘','망최상','굿','엄지','조용','깔끔','적당',
                        '깡패','굉장','아담','완벽','아기자기','고급','최고','세련','만족','아늑','훌륭','예쁘','이쁘','짱','심쿵',
                        '따뜻','깨끗','독특','매력','모던','취향저격','로','마음','클래식','아름','인상적','귀엽','포근','재방문']
        self.neg_dict = ['아쉽','최악','나쁘','느리','빡치','비추','별로','그냥품','낙제','쏘','엉망','실망','불친절','문제',
                         '컴플레인','거지','그닥','그다지','구려','불편','엉성','헬','개판','불친절','똑바로','재수','딱딱하다','차갑다',
                         '별로','다소','나쁘다','바쁘다','어수선하다','이상하다','촌스럽다','거','부담스럽다','시끄럽','복잡',
                         '안','않','못','없','아닌','아니']

    def rv_stemming(self):
        reviews = self.kakao['contents']
        result_list = []
        english = re.compile(r'[a-zA-Z]')

        for i in range(len(reviews)):
            rv = str(reviews[i])

            if len(rv) > 0:
                rv = re.sub(english, "", rv)

                a = re.sub(' ', 's', rv)  # 띄어쓰기 위해 s 붙힘
                b = twitter.pos(a, stem=True, norm=True)  # 형태소 분석
                string = ''
                for word in b:  # 문장으로 합침
                    string += word[0]
                c = re.sub('s', ' ', string)  # 띄어쓰기 분리
                result_list.append(c)
            else:
                result_list.append("")
        self.kakao['contents'] = result_list
        return kakao

    def po_neg_reviews(self):
        kakao = rv_stemming()
        """작업 중 입니다."""
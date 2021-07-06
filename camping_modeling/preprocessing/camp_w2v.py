import pandas as pd
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from konlpy.tag import Okt
from tqdm import tqdm


def word2vec(filename):
    data = pd.read_csv(f'../datas/{filename}.csv', encoding='utf-8-sig', index_col=0)
    data['intro'] = data['intro'].str.replace("&apos;", "")
    data['intro'] = data['intro'].fillna(0)
    data = data[data['intro'] != 0].reset_index(drop=True)

    # 불용어 정의
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '.', ',']

    okt = Okt()
    tokenized_data = []
    for sentence in tqdm(data['intro']):
        temp_X = okt.morphs(sentence, stem=True)  # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
        tokenized_data.append(temp_X)

    model = Word2Vec(sentences=tokenized_data,
                     vector_size=100,
                     window=5,
                     min_count=5,
                     workers=4,
                     sg=0)
    model.wv.save_word2vec_format('../models/camp_w2v.model')  # 모델 저장

def load_model(filename):
    model = KeyedVectors.load_word2vec_format(f'../models/{filename}.model')
    sims = model.most_similar('캠핑장', topn=100)
    return print(sims)


if __name__ == '__main__':
    word2vec('camp_data_merge')
    # load_model('camp_w2v')
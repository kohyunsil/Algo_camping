import pandas as pd
import kakao_review_nlp as nlp
import category_modeling as cm

if __name__ == '__main__':
    s0 = nlp.Review_nlp()
    s1 = cm.CategoryModel()
    # s0.vectorizing()
    # s0.load_model()
    # s0.rv_tokenizing('kakao_review_cat_predict', 'contents')

    # s1.make_cat_predictor('camp_description', 'full_text', 'labels')
    s1.apply_cat_predictor('model2', 'kakao_review_sent', 'review')
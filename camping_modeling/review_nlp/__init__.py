import pandas as pd
import kakao_review_nlp as nlp
import category_modeling as cm

if __name__ == '__main__':
    s0 = nlp.Review_nlp()
    s1 = cm.CategoryModel()
    # s0.vectorizing()
    # s0.load_model()

    s1.apply_cat_predictor()
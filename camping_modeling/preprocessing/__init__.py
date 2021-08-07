import pandas as pd
import camp_api_crawling_merge as cacm
import review_category_modeling as cm
import tag_prior as tp


if __name__ == '__main__':
    # s1 = cm.CategoryModel()
    # s1.rv_cleansing('highlight_review', 'nv')
    # s1.make_cat_predictor('highlight_review', 'category')
    # s1.kk_apply_cat_predictor('review', make_cat_predictor=False)

    # s1.make_cat_predictor('camp_description', 'full_text', 'labels')
    # s1.apply_cat_predictor('model2', 'kakao_review_sent', 'review')

    # merge_preprocessing
    camp_merge = cacm.CampMerge()
    camp_merge.camp_api_data_merge()
    # rp = cacm.ReviewPre()
    # rp.review_preprocessing()

    # merge_result
    merge = cacm.ReviewCamp()
    merge.review_camp_merge()


    #tag-merge
    # tag_df = tp.TagMerge()
    # tag_df.tag_merge()

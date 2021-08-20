import pandas as pd
import re
import config as config


class ReviewInsert:
    def __init__(self):
        self.naver = config.Config.NAVER
        self.kakao = config.Config.KAKAO
        self.camp=config.Config.CAMP

    # 네이버 리뷰 전처리
    def naver_review(self):
        naver = self.naver
        naver['user_info'] = naver['user_info'].str.replace("\n","")
        naver['user_info'] = naver['user_info'].str.replace(" ","")
        naver["user_review"] = naver['user_info'].str.split("리뷰",expand=True)[1].str.split("평균별점",expand=True)[0].str.split("사진",expand=True)[0]
        naver["user_picture"] = naver['user_info'].str.split("사진",expand=True)[1].str.split("평균별점",expand=True)[0]
        naver["user_star"] = naver['user_info'].str.split("평균별점",expand=True)[1]
        naver['date'], naver['visit'] = naver["visit_info"].str.split(" ",1).str
        naver['visit_date'] = naver['date'].str[:10]
        naver['visit_count'] = naver['date'].str[10:] + naver['visit'].str[:2]
        naver['visit_count'] = naver['visit_count'].str.split('').str[1]
        naver['visit_reservation'] = naver['visit'].str[2:]
        naver = naver.drop(['user_info', 'visit_info', 'date', 'visit'],1)
        naver['platform'] = 1
        naver = naver.drop(['addr'],1)
        naver = naver.rename(columns={'title' : 'place_name', 
                                    'user_name' : 'user_nickname', 
                                    'visit_date' : 'date', 
                                    'base_addr' : 'addr', 
                                    'user_picture' : 'photo_cnt',
                                    'highlight_review' : 'contents', 
                                    'category' : 'cat_tag', 
                                    'visit_count' : 'visit_cnt', 
                                    'user_review' : 'review_cnt',
                                    'user_star' : 'mean_star'})
        return naver

    # 카카오 리뷰 전처리
    def kakao_review(self):
        kakao = self.kakao
        kakao['platform'] = 0
        kakao = kakao.rename(columns={'kakaoMapUserId' : 'user_id', 'point' : 'star', 'likeCnt' : 'like_cnt', 
                                'photoCnt' : 'photo_cnt', 'username' : 'user_nickname'})
        return kakao
    
    # 네이버와 카카오 리뷰 concat
    def review_dataset(self, camp_df):
        naver = self.naver_review()
        kakao = self.kakao_review()
        kakao_naver = pd.concat([naver, kakao], 0)
        review_data = camp_df[['place_id', 'place_name']]
        review_data_df = pd.merge(review_data, kakao_naver, left_on='place_name', right_on='place_name', how="right")
        review_data_df = review_data_df.drop_duplicates()
        review_data_df = review_data_df.reset_index()
        review_data_df = review_data_df.rename(columns={'index' : 'id', 'userId' : 'user_id', })
        return review_data_df

    # review table
    def review_table(self, review_data_df):
        review_df = review_data_df[['platform', 'user_id', 'place_id', 'like_cnt', 'photo_cnt', 'date', 'cat_tag', 
                            'star', 'contents']]
        review_df = review_df.dropna(subset = ['place_id'])
        return review_df

    # reviewer table
    def reviewer_table(self, review_data_df):
        reviewer = review_data_df[['id', 'platform', 'user_nickname', 'mean_star', 'visit_cnt', 'review_cnt']]
        reviewer_df = reviewer.rename(columns={'id' : 'review_id'})
        reviewer_df['visit_cnt'] = reviewer_df['visit_cnt'].str.split('').str[1]
        return reviewer_df


            

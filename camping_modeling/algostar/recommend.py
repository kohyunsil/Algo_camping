import camp_api_crawling_merge as cacm
import tag_points as tp
import config as config
import pandas as pd

class ProfilePro:

    def __init__(self):
        self.df = config.Config.API_DATA
        self.cdf = cacm.ReviewCamp().review_camp_merge()
        self.tdf = tp.TagMerge().tag_merge()

    def animal_camp(self):
        ''' 반려동물 동반여부'''
        animal_df = self.df[['contentId','facltNm','animalCmgCl','firstImageUrl']]
        all_animal = animal_df[animal_df.animalCmgCl == '가능'].reset_index(drop=True)
        small_animal = animal_df[animal_df.animalCmgCl == '가능(소형견)'].reset_index(drop=True)
        impossibility = animal_df[animal_df.animalCmgCl == '불가능'].reset_index(drop=True)
        return all_animal, small_animal, impossibility

    def induty_camp(self):
        ''' 업종에 따라 분류한 선호캠핑 스타일
            1. auto_car = 오토캠핑
            2. glam_cara = 카라반, 글램핑'''
        induty_df = self.df[['contentId','facltNm','firstImageUrl','induty']]
        auto_car = induty_df[induty_df['induty'].str.startswith(('일반야영장', '자동차야영장'))].reset_index(drop=True).drop('induty',1)
        glam_cara = induty_df[induty_df['induty'].str.contains(('카라반|글램핑'))].reset_index(drop=True).drop('induty', 1)
        return auto_car, glam_cara

    def purpose_camp(self):
        """ 캠핑 목적 1. 스트레스 해소(액티비티, 관광, 물놀이)
                    2. 친목 도모(가족, 친구, 연인과 즐기는 캠핑)
                    3. 자연 체험(생태교육, 아이동반 등)
                    4. 여유로운 힐링(휴양, 별 감상 등)
                    5. 캠핑족(캠핑은 나의 취미) """
        purpose_df = self.df[['contentId','facltNm','firstImageUrl','themaEnvrnCl','intro']]

        # 1. stress_relief (태그-축제)
        tour_df = purpose_df[purpose_df['intro'].str.contains('관광지|관광', na=False)].reset_index(drop=True).iloc[:, :3]
        activity_df = purpose_df[purpose_df['themaEnvrnCl'].str.contains('액티비티|항공레저|물놀이|명소', na=False)].reset_index(drop=True).iloc[:, :3]
        stress_df = pd.merge(tour_df, activity_df, how='inner', on ='contentId')

        # 2. 친목 도모 (태그 - 가족, 커플)
        withs = self.cdf[['camp', 'contentId', 'with_family_s', 'with_couple_s']]
        with_df = withs[(withs['with_family_s'] == 1) | (withs['with_couple_s'] == 1)].reset_index(drop=True).iloc[:, :2]
        with_final_df = pd.merge(purpose_df, with_df, how='inner', on='contentId').iloc[:, :3].dropna(subset=['firstImageUrl']).reset_index(drop=True)

        # 3. 자연 체험 (태그-생태교육, 문화유적, 둘레길/ 테마-명소(가을단풍,겨울눈꽃), 걷기길)
        env_intro = purpose_df[purpose_df['intro'].str.contains('자연|체험|학습', na=False)].reset_index(drop=True).iloc[:, :3]
        env_thema = purpose_df[purpose_df['themaEnvrnCl'].str.contains('명소|걷기길', na=False)].reset_index(drop=True).iloc[:, :3]
        env_df = pd.merge(env_thema, env_intro, how='inner', on='contentId').reset_index(drop=True).iloc[:, :3].rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'})
        field_tag = self.cdf[['camp', 'contentId', 'ecological_s', 'cultural_s', 'trail_s']]
        field_tags = field_tag[(field_tag['ecological_s'] == 1) | (field_tag['cultural_s'] == 1) | (field_tag['trail_s'] == 1)].reset_index(drop=True).iloc[:, :2]
        field_trip = pd.merge(env_df, field_tags, how='inner', on='contentId').reset_index(drop=True).iloc[:, :3].dropna(subset=['firstImageUrl'])

        # 4. 여유로운 힐링 (태그 - 여유있는, 계곡옆, 물맑은, 별 보기 좋은, 힐링, 그늘이 많은, 바다가 보이는)
        healing_df = self.tdf[['camp', 'contentId', 'relax_s', 'valley_s', 'pure_water_s', 'star_s', 'healing_s', 'shade_s', 'ocean_s']]
        heal_cols = healing_df.columns.tolist()[2:]
        for heal_col in heal_cols:
            healing_dfs = healing_df[[healing_df[f'{heal_col}'] == 1]

        # 5. 캠핑족

        return stress_df, with_final_df, field_trip, print(healing_dfs)



if __name__ == '__main__':
    c = ProfilePro()
    # c.animal_camp()
    # c.induty_camp()
    c.purpose_camp()


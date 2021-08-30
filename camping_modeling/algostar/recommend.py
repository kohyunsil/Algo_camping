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
        animal_df = self.df[['contentId','facltNm','firstImageUrl', 'animalCmgCl']]
        all_animal = animal_df[animal_df.animalCmgCl == '가능'].dropna(subset=['firstImageUrl']).reset_index(drop = True).iloc[:, :3]
        small_animal = animal_df[animal_df.animalCmgCl == '가능(소형견)'].dropna(subset=['firstImageUrl']).reset_index(drop = True)
        impossibility = animal_df[animal_df.animalCmgCl == '불가능'].dropna(subset=['firstImageUrl']).reset_index(drop = True)
        return {'all_animal':all_animal, 'small_animal':small_animal, 'impossibility':impossibility}

    def induty_camp(self):
        ''' 업종에 따라 분류한 선호캠핑 스타일
            1. auto_car = 오토캠핑
            2. glam_cara = 카라반, 글램핑'''
        induty_df = self.df[['contentId','facltNm','firstImageUrl','induty']]
        auto_car = induty_df[induty_df['induty'].str.startswith(('일반야영장', '자동차야영장'))].reset_index(drop=True).drop('induty',1)
        glam_cara = induty_df[induty_df['induty'].str.contains(('카라반|글램핑'))].reset_index(drop=True).drop('induty', 1)
        return {'auto_car':auto_car, 'glam_cara':glam_cara, 'etc':induty_df.iloc[:, :3]}

    def purpose_camp(self):
        """ 캠핑 목적 1. 스트레스 해소(액티비티, 관광, 물놀이)
                    2. 친목 도모(가족, 친구, 연인과 즐기는 캠핑)
                    3. 자연 체험(생태교육, 아이동반 등)
                    4. 여유로운 힐링(휴양, 별 감상 등)
                    5. 캠핑족(캠핑은 나의 취미) """
        purpose_df = self.df[['contentId','facltNm','firstImageUrl','themaEnvrnCl','intro','brazierCl']]

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
        healing_df = self.tdf[['camp', 'contentId', 'relax_s', 'valley_s', 'pure_water_s', 'star_s', 'healing_s', 'shade_s']]
        healing_tags = healing_df[(healing_df['relax_s'] == 1) | (healing_df['valley_s'] == 1) | (healing_df['pure_water_s'] == 1)
                       | (healing_df['star_s'] == 1) | (healing_df['healing_s'] == 1) | (healing_df['shade_s'] == 1)].reset_index(drop=True).iloc[:, :2]
        healing_thema = purpose_df[purpose_df['themaEnvrnCl'].str.contains('명소|걷기길', na=False)].reset_index(drop=True).iloc[:, :3]
        healing_intro = purpose_df[purpose_df['intro'].str.contains('힐링|휴양|전망', na=False)].reset_index(drop=True).iloc[:, :3]
        healing_fire = purpose_df[purpose_df['brazierCl'].str.contains('개별', na=False)].reset_index(drop=True).iloc[:, :3]
        healing_merge_df = pd.merge(healing_intro, healing_thema, how='inner', on='contentId').iloc[:, :3]
        healing_merge_df2 = pd.merge(healing_merge_df, healing_fire, how='inner', on='contentId').iloc[:, :3]
        healing_final_df = pd.merge(healing_merge_df2, healing_tags, how='inner', on='contentId').iloc[:, :3]

        return {'stress_df':stress_df, 'with_final_df':with_final_df, 'field_trip':field_trip, 'healing_final_df':healing_final_df}

    def final_merge(self, animal, induty, purpose):

        data1 = self.animal_camp()[f'{animal}']
        data2 = self.induty_camp()[f'{induty}']
        data3 = self.purpose_camp()[f'{purpose}']

        datas = pd.merge(data1, data2, how='inner', on='contentId').iloc[:,:3].rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'}).dropna(subset=['firstImageUrl']).reset_index(drop=True)
        final_df = pd.merge(datas, data3, how='inner', on='contentId').iloc[:,:3].rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'}).dropna(subset=['firstImageUrl']).reset_index(drop=True)
        return final_df

class BeforeLogin:

    def __init__(self):
        self.df = config.Config.API_DATA
        self.tdf = tp.TagMerge().tag_merge()

    def camp_thema(self):

        data_df = self.df[['contentId', 'facltNm', 'firstImageUrl', 'tourEraCl', 'lctCl']]
        def thema_select(column, value):
            data = data_df[data_df[f'{column}'].str.contains(f'{value}', na = False)].dropna(subset=['firstImageUrl']).reset_index(drop = True)
            return data

        #season
        all_season = thema_select('tourEraCl','봄,여름,가을,겨울').iloc[:, :3]
        spring = thema_select('tourEraCl','봄').iloc[:, :3]
        summer = thema_select('tourEraCl','여름').iloc[:, :3]
        fall = thema_select('tourEraCl', '가을').iloc[:, :3]
        winter = thema_select('tourEraCl', '겨울').iloc[:, :3]

        #주변환경
        beach = thema_select('lctCl', '해변').iloc[:, :3]
        river = thema_select('lctCl','강').iloc[:, :3]
        downtown = thema_select('lctCl','도심').iloc[:, :3]
        lake = thema_select('lctCl','호수').iloc[:, :3]
        mountain = thema_select('lctCl','산').iloc[:, :3]
        valley = thema_select('lctCl','계곡').iloc[:, :3]
        forest = thema_select('lctCl','숲').iloc[:, :3]

        return {'all_season':all_season, 'spring':spring, 'summer':summer, 'fall':fall, 'winter':winter, 'beach':beach,
                'river':river, 'downtown': downtown, 'lake':lake, 'mountain':mountain, 'valley':valley, 'forest':forest}
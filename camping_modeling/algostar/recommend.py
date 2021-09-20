import camp_api_crawling_merge as cacm
import algo_config as config
import tag_points as tp
import camping_modeling.apis.gocamping_api as ga
gocamping = ga.GocampingApi()
import pandas as pd

class BeforeLogin:

    def __init__(self):
        self.df = gocamping.gocampingAPI()
        self.df['contentId'] = self.df['contentId'].astype('int64')
        self.cdf = cacm.ReviewCamp().review_camp_merge()
        self.tdf = tp.TagMerge().tag_merge()

    def camp_thema(self):

        data_df = self.df[['contentId', 'facltNm', 'firstImageUrl', 'tourEraCl', 'lctCl']]
        def thema_select(column, value):
            data = data_df[data_df[f'{column}'].str.contains(f'{value}', na = False)].dropna(subset=['firstImageUrl']).reset_index(drop = True)
            return data

        '''계절별 캠핑장'''
        all_season = thema_select('tourEraCl','봄,여름,가을,겨울').iloc[:, :3]
        spring = thema_select('tourEraCl','봄').iloc[:, :3]
        summer = thema_select('tourEraCl','여름').iloc[:, :3]
        fall = thema_select('tourEraCl', '가을').iloc[:, :3]
        winter = thema_select('tourEraCl', '겨울').iloc[:, :3]

        '''캠핑장 주변환경 별 캠핑장리스트'''
        beach = thema_select('lctCl', '해변').iloc[:, :3]
        mountain_valley = thema_select('lctCl','산|계곡').iloc[:, :3]
        lake_river = thema_select('lctCl','강|호수').iloc[:, :3]
        downtown = thema_select('lctCl','도심').iloc[:, :3]
        # lake = thema_select('lctCl','호수').iloc[:, :3]
        # valley = thema_select('lctCl','계곡').iloc[:, :3]
        # forest = thema_select('lctCl','숲').iloc[:, :3]

        return {'all_season':all_season, 'spring':spring, 'summer':summer, 'fall':fall, 'winter':winter, 'beach':beach,
                'mountain_valley':mountain_valley, 'lake_river':lake_river, 'downtown': downtown}

class ProfilePro(BeforeLogin):

    def __init__(self):
        super().__init__()

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

    def together_camp(self, value, column='with_family_s'):
        together_df = self.cdf[['camp', 'contentId', 'with_family_s', 'with_couple_s']]
        api_df = self.df[['contentId','facltNm','firstImageUrl','intro']]
        with_column = together_df[together_df[f'{column}'] == 1].reset_index(drop=True).iloc[:, :2]
        api_value = api_df[api_df['intro'].str.contains(f'{value}', na=False)].reset_index(drop=True).iloc[:, :3]
        df = pd.merge(with_column, api_value, how='outer', on ='contentId').iloc[:, 1:4].dropna(subset=['firstImageUrl']).reset_index(drop=True)

        return {'df':df, 'alone_df':api_value}

    def purpose_camp(self):

        """ 캠핑 목적 1. 아이와 함께 즐기는 캠핑 : (아이들 놀기 좋은, 물놀이, 생태교육)
                    2. 여유롭게 즐기는 감성 캠핑  : (휴양, 별 감상 등)
                    3. 체험하며 즐기는 캠핑 : (생태교육, 액티비티, 물놀이)
                    4. 방방곡곡 투어형 캠핑 :  주변 즐길거리 (관광, 지역축제) """

        purpose_df = self.df[['contentId','facltNm','firstImageUrl','themaEnvrnCl','intro','brazierCl']]

        # 1. 아이와 함께 즐기는 캠핑 (아이들 놀기 좋은, 물놀이, 생태교육)
        child_tdf = self.tdf[['camp', 'contentId', 'childlike_r', 'with_child_s', 'ecological_s']]
        child_df = child_tdf[(child_tdf['childlike_r'] == 1) | (child_tdf['with_child_s'] == 1) | (child_tdf['ecological_s'] == 1)].reset_index(drop = True).iloc[:, :2]
        with_child_df = pd.merge(purpose_df, child_df, how = 'inner', on = 'contentId').iloc[:, :3].dropna(subset = ['firstImageUrl']).reset_index(drop = True)
        kids_df = purpose_df[purpose_df['intro'].str.contains('아이|물놀이|아이들', na=False)].reset_index(drop=True).iloc[:, :3]
        kids_camp = pd.merge(with_child_df, kids_df, how='inner', on='contentId').reset_index(drop=True).iloc[:, :3].rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'})

        # 2. 여유롭게 즐기는 감성 캠핑  : (휴양, 별 감상 등)
        healing_df = self.tdf[['camp', 'contentId', 'relax_s', 'valley_s', 'pure_water_s', 'star_s', 'healing_s', 'shade_s']]
        healing_tags = healing_df[(healing_df['relax_s'] == 1) | (healing_df['valley_s'] == 1) | (healing_df['pure_water_s'] == 1)
                       | (healing_df['star_s'] == 1) | (healing_df['healing_s'] == 1) | (healing_df['shade_s'] == 1)].reset_index(drop=True).iloc[:, :2]
        healing_thema = purpose_df[purpose_df['themaEnvrnCl'].str.contains('명소|걷기길', na=False)].reset_index(drop=True).iloc[:, :3]
        healing_intro = purpose_df[purpose_df['intro'].str.contains('힐링|휴양|전망', na=False)].reset_index(drop=True).iloc[:, :3]
        healing_fire = purpose_df[purpose_df['brazierCl'].str.contains('개별', na=False)].reset_index(drop=True).iloc[:, :3]
        healing_merge_df = pd.merge(healing_intro, healing_thema, how='inner', on='contentId').iloc[:, :3]
        healing_merge_df2 = pd.merge(healing_merge_df, healing_fire, how='inner', on='contentId').iloc[:, :3]
        healing_camp = pd.merge(healing_merge_df2, healing_tags, how='inner', on='contentId').iloc[:, :3].rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'})

        # 3. 체험하며 즐기는 캠핑 : (생태교육, 액티비티, 물놀이)
        exp_intro = purpose_df[purpose_df['intro'].str.contains('자연|체험|학습|물놀이', na=False)].reset_index(drop=True).iloc[:, :3]
        exp_thema = purpose_df[purpose_df['themaEnvrnCl'].str.contains('액티비티|항공레저|물놀이', na = False)].reset_index(drop = True).iloc[:, :3]
        exp_df = pd.merge(exp_thema, exp_intro, how='inner', on='contentId').reset_index(drop=True).iloc[:, :3].rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'})
        field_tag = self.cdf[['camp', 'contentId', 'extreme_s', 'exciting_r', 'ecological_s']]
        field_tags = field_tag[(field_tag['extreme_s'] == 1) | (field_tag['exciting_r'] == 1) | (field_tag['ecological_s'] == 1)].reset_index(drop=True).iloc[:, :2]
        field_trip = pd.merge(exp_df, field_tags, how='inner', on='contentId').reset_index(drop=True).iloc[:, :3].dropna(subset=['firstImageUrl'])

        # 4. 방방곡곡 투어형 캠핑 (축제, 관광지)
        tour_tag = self.tdf[['camp', 'contentId', 'festival_s', 'cultural_s']]
        tour_tags = tour_tag[(tour_tag['festival_s'] == 1) | (tour_tag['cultural_s'] == 1)].reset_index(drop = True).iloc[:, :2]
        tour_df = purpose_df[purpose_df['intro'].str.contains('관광지|관광|축제', na=False)].reset_index(drop=True).iloc[:, :3]
        tour_df2 = purpose_df[purpose_df['themaEnvrnCl'].str.contains('명소|걷기길', na=False)].reset_index(drop=True).iloc[:, :3]
        tour_camps = pd.merge(tour_df, tour_df2, how='inner', on='contentId')
        tour_camp = pd.merge(tour_tags, tour_camps, how='inner', on='contentId').reset_index(drop=True).iloc[:, 1:4].rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'}).dropna(subset=['firstImageUrl'])
        tour_camp['contentId'] = tour_camp['contentId'].astype('int64')

        return {'kids_camp': kids_camp, 'healing_camp':healing_camp, 'field_trip':field_trip, 'tour_camp':tour_camp}

    def final_merge(self, animal, induty, season, around, purpose):

        """
        설문항목 1 캠핑을 1년에 몇 번 가시나요? > x
        설문항목 2 누구와 함께 가시나요? > df2
        설문항목 2-1 반려동물과 함께 하시나요? > df2_1
        설문항목 3 선호하는 캠핑 스타일을 골라주세요 (사진대체) > df3
        설문항목 4-1 캠핑가기 딱 좋은 계절은? df4_1
        설문항목 4-2 어디 근처에서 캠핑하는 걸 좋아하세요? df4_2
        설문항목 5 캠핑 취향 설문? > df5
        설문항목 6 선호하는 지역은? > df6
        """

        # df2 = self.together_camp()[f'{together}']
        df2_1 = self.animal_camp()[f'{animal}'] #all_animal, small_animal, impossibility
        df3 = self.induty_camp()[f'{induty}']  #auto_car, glam_cara, induty_camp
        df4_1 = self.camp_thema()[f'{season}'] #spring, summer, fall, winter
        df4_2 = self.camp_thema()[f'{around}'] #beach, mountain_valley, lake_river, downtown
        df5 = self.purpose_camp()[f'{purpose}'] #kids_camp, healing_camp, field_trip, tour_camp


        datas = pd.merge(df2_1, df3, how='inner', on='contentId').iloc[:,:3].rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'}).dropna(subset=['firstImageUrl']).reset_index(drop=True)
        final_df = pd.merge(df, df4, how='inner', on='contentId').iloc[:,:3].rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'}).dropna(subset=['firstImageUrl']).reset_index(drop=True)

        return final_df

if __name__ == '__main__':
    profile = ProfilePro()
    b_login = BeforeLogin()

    # print(profile.animal_camp()['all_animal'])
    # print(profile.induty_camp()['auto_car'])

    # print(profile.together_camp('가족|친구')['df'])
    # print(profile.together_camp('부부|연인', 'with_couple_s')['df'])
    # print(profile.together_camp('혼자')['alone_df'])

    # print(profile.purpose_camp()['kids_camp']) # 428 rows
    # print(profile.purpose_camp()['healing_camp']) # 236 rows
    # print(profile.purpose_camp()['field_trip']) # 238 rows
    # print(profile.purpose_camp()['tour_camp']) # 180 rows


    # print(profile.final_merge('all_animal', 'etc', 'healing_final_df'))


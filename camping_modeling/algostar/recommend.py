import camp_api_crawling_merge as cacm
import algo_config as config
import tag_points as tp
import camping_modeling.apis.gocamping_api as ga
gocamping = ga.GocampingApi()
import pandas as pd
from functools import reduce

class BeforeLogin:

    def __init__(self):
        self.df = gocamping.gocampingAPI()
        self.df['contentId'] = self.df['contentId'].astype('int64')
        self.cdf = cacm.ReviewCamp().review_camp_merge()
        self.tdf = tp.TagMerge().tag_merge()

    def thema_select(self, df, column, value):
        data = df[df[f'{column}'].str.contains(f'{value}', na = False)].reset_index(drop=True).iloc[:, :3].dropna(subset=['firstImageUrl'])
        return data

    def merge_df(self, df1, df2):
        df = pd.merge(df1, df2, how='inner', on ='contentId').reset_index(drop=True).iloc[:, :3]
        return df

    def camp_thema(self):

        data_df = self.df[['contentId', 'facltNm', 'firstImageUrl', 'tourEraCl', 'lctCl']]

        '''계절별 캠핑장'''
        # all_season = thema_select('tourEraCl','봄,여름,가을,겨울')
        spring = self.thema_select(data_df, 'tourEraCl','봄')
        summer = self.thema_select(data_df, 'tourEraCl','여름')
        fall = self.thema_select(data_df, 'tourEraCl', '가을')
        winter = self.thema_select(data_df, 'tourEraCl', '겨울')

        '''캠핑장 주변환경 별 캠핑장리스트'''
        beach = self.thema_select(data_df, 'lctCl', '해변')
        mountain_valley = self.thema_select(data_df, 'lctCl','산|계곡')
        lake_river = self.thema_select(data_df, 'lctCl','강|호수')
        downtown = self.thema_select(data_df, 'lctCl','도심')
        # lake = thema_select('lctCl','호수')
        # valley = thema_select('lctCl','계곡')
        # forest = thema_select('lctCl','숲')

        return {'spring':spring, 'summer':summer, 'fall':fall, 'winter':winter, 'beach':beach,
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
        glam_cara = self.thema_select(induty_df, 'induty', '카라반|글램핑')
        return {'auto_car':auto_car, 'glam_cara':glam_cara, 'etc':induty_df.iloc[:, :3]}

    def together_camp(self, value):
        together_df = self.cdf[['camp', 'contentId', 'with_family_s', 'with_couple_s']]
        api_df = self.df[['contentId','facltNm','firstImageUrl','intro']]
        with_family = together_df[together_df['with_family_s'] == 1].reset_index(drop=True).iloc[:, :2]
        with_couple = together_df[together_df['with_couple_s'] == 1].reset_index(drop=True).iloc[:, :2]
        api_value = self.thema_select(api_df, 'intro', f'{value}')
        with_family_df = pd.merge(with_family, api_value, how='outer', on ='contentId').iloc[:, 1:4].dropna(subset=['firstImageUrl']).reset_index(drop=True)
        with_couple_df = pd.merge(with_couple, api_value, how='outer', on ='contentId').iloc[:, 1:4].dropna(subset=['firstImageUrl']).reset_index(drop=True)
        return {'with_family_df':with_family_df, 'with_couple_df':with_couple_df,'alone_df':api_value}

    def purpose_camp(self):


        """ 캠핑 목적 1. 아이와 함께 즐기는 캠핑 : (아이들 놀기 좋은, 물놀이, 생태교육)
                    2. 여유롭게 즐기는 감성 캠핑  : (휴양, 별 감상 등)
                    3. 체험하며 즐기는 캠핑 : (생태교육, 액티비티, 물놀이)
                    4. 방방곡곡 투어형 캠핑 :  주변 즐길거리 (관광, 지역축제) """

        purpose_df = self.df[['contentId','facltNm','firstImageUrl','themaEnvrnCl','intro','brazierCl']]

        # 1. 아이와 함께 즐기는 캠핑 (아이들 놀기 좋은, 물놀이, 생태교육)
        child_tdf = self.tdf[['camp', 'contentId', 'childlike_r', 'with_child_s', 'ecological_s']]
        child_df = child_tdf[(child_tdf['childlike_r'] == 1) | (child_tdf['with_child_s'] == 1) | (child_tdf['ecological_s'] == 1)].reset_index(drop = True).iloc[:, :2]
        with_child_df = self.merge_df(purpose_df, child_df)
        kids_df = self.thema_select(purpose_df, 'intro', '아이|물놀이|아이들')
        kids_camp = self.merge_df(with_child_df, kids_df).rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'}).dropna(subset = ['firstImageUrl'])

        # 2. 여유롭게 즐기는 감성 캠핑  : (휴양, 별 감상 등)
        healing_df = self.tdf[['camp', 'contentId', 'relax_s', 'valley_s', 'pure_water_s', 'star_s', 'healing_s', 'shade_s']]
        healing_tags = healing_df[(healing_df['relax_s'] == 1) | (healing_df['valley_s'] == 1) | (healing_df['pure_water_s'] == 1)
                       | (healing_df['star_s'] == 1) | (healing_df['healing_s'] == 1) | (healing_df['shade_s'] == 1)].reset_index(drop=True).iloc[:, :2]
        healing_thema = self.thema_select(purpose_df, 'themaEnvrnCl', '명소|걷기길')
        healing_intro = self.thema_select(purpose_df, 'intro', '힐링|휴양|전망')
        healing_fire = self.thema_select(purpose_df, 'brazierCl', '개별')
        healing_merge_df = self.merge_df(healing_intro, healing_thema)
        healing_merge_df2 = self.merge_df(healing_merge_df, healing_fire)
        healing_camp = self.merge_df(healing_merge_df2, healing_tags).rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'}).dropna(subset = ['firstImageUrl'])

        # 3. 체험하며 즐기는 캠핑 : (생태교육, 액티비티, 물놀이)
        exp_intro = self.thema_select(purpose_df, 'intro', '자연|체험|학습|물놀이')
        exp_thema = self.thema_select(purpose_df, 'themaEnvrnCl', '액티비티|항공레저|물놀이')
        exp_df = self.merge_df(exp_thema, exp_intro)
        field_tag = self.cdf[['camp', 'contentId', 'extreme_s', 'exciting_r', 'ecological_s']]
        field_tags = field_tag[(field_tag['extreme_s'] == 1) | (field_tag['exciting_r'] == 1) | (field_tag['ecological_s'] == 1)].reset_index(drop=True).iloc[:, :2]
        field_trip = self.merge_df(exp_df, field_tags).rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'}).dropna(subset = ['firstImageUrl'])

        # 4. 방방곡곡 투어형 캠핑 (축제, 관광지)
        tour_tag = self.tdf[['camp', 'contentId', 'festival_s', 'cultural_s']]
        tour_tags = tour_tag[(tour_tag['festival_s'] == 1) | (tour_tag['cultural_s'] == 1)].reset_index(drop = True).iloc[:, :2]
        tour_df = self.thema_select(purpose_df, 'intro', '관광지|관광|축제')
        tour_df2 = self.thema_select(purpose_df, 'themaEnvrnCl', '명소|걷기길')
        tour_camps = self.merge_df(tour_df, tour_df2)
        tour_camp = self.merge_df(tour_camps, tour_tags).rename(columns={'facltNm_x':'facltNm', 'firstImageUrl_x':'firstImageUrl'}).dropna(subset = ['firstImageUrl'])
        tour_camp['contentId'] = tour_camp['contentId'].astype('int64')

        return {'kids_camp':kids_camp, 'healing_camp':healing_camp, 'field_trip':field_trip, 'tour_camp':tour_camp}

    def region_camp(self):
        region_df = self.df[['contentId','facltNm','firstImageUrl','doNm']]

        # 수도권 (서울시/경기도/인천시)
        region_1 = self.thema_select(region_df, 'doNm', '서울시|경기도|인천시').reset_index(drop=True)
        # 동해/강원권 (강원도)
        region_2 = self.thema_select(region_df, 'doNm', '강원도').reset_index(drop=True)
        # 남해/영남권 (경상남도/경상북도/대구시/부산시/울산시)
        region_3 = self.thema_select(region_df, 'doNm', '경상남도|경상북도|대구시|부산시|울산시').reset_index(drop=True)
        # 서해/충청권 (대전시/세종시/충청북도/충청남도)
        region_4 = self.thema_select(region_df, 'doNm', '대전시|세종시|충청북도|충청남도').reset_index(drop=True)
        # 호남권 (광주시/전라남도/전라북도)
        region_5 = self.thema_select(region_df, 'doNm', '광주시|전라남도|전라북도').reset_index(drop=True)
        # 제주도
        region_6 = self.thema_select(region_df, 'doNm', '제주도').reset_index(drop=True)

        return {'region_1':region_1, 'region_2':region_2, 'region_3':region_3, 'region_4':region_4, 'region_5':region_5, 'region_6':region_6}


    def final_merge(self, value, together, animal, induty, season, around, purpose, region):

        """
        설문항목 2 누구와 함께 가시나요? > df1
        설문항목 2-1 반려동물과 함께 하시나요? > df2
        설문항목 3 선호하는 캠핑 스타일을 골라주세요 (사진대체) > df3
        설문항목 4-1 캠핑가기 딱 좋은 계절은? df4
        설문항목 4-2 어디 근처에서 캠핑하는 걸 좋아하세요? df5
        설문항목 5 캠핑 취향 설문? > df6
        설문항목 6 선호하는 지역은? > region_df
        """

        df1 = self.together_camp(f'{value}')[f'{together}']
        df2 = self.animal_camp()[f'{animal}']               #all_animal, small_animal, impossibility
        df3 = self.induty_camp()[f'{induty}']               #auto_car, glam_cara, induty_camp
        df4 = self.camp_thema()[f'{season}']                #spring, summer, fall, winter
        df5 = self.camp_thema()[f'{around}']                #beach, mountain_valley, lake_river, downtown
        df6 = self.purpose_camp()[f'{purpose}']             #kids_camp, healing_camp, field_trip, tour_camp

        profile_df = [df1, df2, df3, df4, df5, df6]
        profile_df.sort(key = len, reverse = True)

        merged_profile_df = reduce(lambda x, y: pd.merge(x, y, how = 'left', on = 'contentId'), profile_df)
        merged_profile_final = pd.concat([merged_profile_df.contentId, merged_profile_df.iloc[:, 11:]], 1)

        region_df = self.region_camp()[f'{region}']
        merge_df_f = pd.merge(region_df, merged_profile_final, how='left', on='contentId')
        merge_df_f = pd.concat([merge_df_f.contentId, merge_df_f.iloc[:, 4:]], 1).rename(columns={'facltNm_y':'facltNm', 'firstImageUrl_y':'firstImageUrl'}).dropna(subset = ['firstImageUrl'])

        return merge_df_f


if __name__ == '__main__':
    profile = ProfilePro()
    b_login = BeforeLogin()

    # print(b_login.camp_thema()['downtown'])

    # print(profile.animal_camp()['all_animal'])
    # print(profile.induty_camp()['glam_cara'])

    # print(profile.together_camp('가족|친구|동료')['with_family_df'])
    # print(profile.together_camp('부부|커플|연인|2인')['with_couple_df'])
    # print(profile.together_camp('혼자')['alone_df'])

    # print(profile.purpose_camp()['kids_camp']) # 428 rows
    # print(profile.purpose_camp()['healing_camp']) # 232 rows
    # print(profile.purpose_camp()['field_trip']) # 237 rows
    # print(profile.purpose_camp()['tour_camp']) # 180 rows

    # print(profile.region_camp()['region_1']) #546 rows
    # print(profile.region_camp()['region_2']) #443 rows


    print(profile.final_merge('가족|친구|동료', 'with_family_df', 'all_animal', 'auto_car', 'spring', 'mountain_valley', 'field_trip', 'region_1'))


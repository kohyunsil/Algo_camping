import pandas as pd
import algo_config as config
import recommend as reco
import camping_modeling.apis.gocamping_api as ga
gocamping = ga.GocampingApi()

class UserWeights(reco.ProfilePro):

    def __init__(self):
        super().__init__()
        self.eda_df = self.df[['contentId', 'facltNm', 'brazierCl', 'doNm', 'caravAcmpnyAt', 'induty', 'operPdCl', 'posblFcltyCl', 'themaEnvrnCl', 'tourEraCl', 'lctCl', 'lineIntro', 'intro']]

    def reco_A200(self):
        '''1. 가족 / 2. 친구동료 / 3. 부부, 연인 / 4. 혼자'''

        family = self.together_camp('가족')['with_family_df'].iloc[:, :1]
        family = pd.merge(self.eda_df, family, how='inner', on='contentId')

        friends = self.together_camp('친구|동료')['alone_df'].iloc[:, :1]
        friends = pd.merge(self.eda_df, friends, how='inner', on='contentId')

        couple = self.together_camp('부부|커플|연인|2인')['with_couple_df'].iloc[:, :1]
        couple = pd.merge(self.eda_df, couple, how='inner', on='contentId')

        alone = self.together_camp('혼자')['alone_df'].iloc[:, :1]
        alone = pd.merge(self.eda_df, alone, how='inner', on='contentId')

        return {'family':family, 'friends':friends, 'couple':couple, 'alone':alone}

    def reco_A210(self):
        '''1. 함께해요 / 2. 아니에요'''

        animal = pd.concat([self.animal_camp()['all_animal'], self.animal_camp()['small_animal']],0).iloc[:, :1]
        animal = pd.merge(self.eda_df, animal, how='inner', on='contentId')

        non_animal = self.animal_camp()['impossibility'].iloc[:, :1]
        non_animal = pd.merge(self.eda_df, non_animal, how='inner', on='contentId')


        return {'animal':animal, 'impossibility':non_animal}

    def reco_A300(self):
        ''' 1. 오토캠핑 / 2. 글램핑,카라반 / 3. 오지캠핑 '''

        auto_car = self.induty_camp()['auto_car'].iloc[:, :1]
        auto_car = pd.merge(self.eda_df, auto_car, how='inner', on='contentId')

        glam_cara = self.induty_camp()['glam_cara'].iloc[:, :1]
        glam_cara = pd.merge(self.eda_df, glam_cara, how='inner', on='contentId')

        etc = self.induty_camp()['etc'].iloc[:, :1]
        etc = pd.merge(self.eda_df, etc, how='inner', on='contentId')

        return {'auto_car' : auto_car, 'glam_cara':glam_cara, 'etc':etc}

    def reco_A410(self):
        ''' 1. 봄 / 2. 여름 / 3. 가을 / 4. 겨울 '''

        spring = self.camp_thema()['spring'].iloc[:, :1]
        spring = pd.merge(self.eda_df, spring, how='inner', on='contentId')

        summer = self.camp_thema()['summer'].iloc[:, :1]
        summer = pd.merge(self.eda_df, summer, how='inner', on='contentId')

        fall = self.camp_thema()['fall'].iloc[:, :1]
        fall = pd.merge(self.eda_df, fall, how='inner', on='contentId')

        winter = self.camp_thema()['winter'].iloc[:, :1]
        winter = pd.merge(self.eda_df, winter, how='inner', on='contentId')

        return {'spring':spring, 'summer':summer, 'fall':fall, 'winter':winter}

    def reco_A420(self):
        ''' 1. 바다,해수욕장 / 2. 산,계곡 / 3. 강,호수 / 4. 도심 '''

        beach = self.camp_thema()['beach'].iloc[:, :1]
        beach = pd.merge(self.eda_df, beach, how='inner', on='contentId')

        mountain_valley = self.camp_thema()['mountain_valley'].iloc[:, :1]
        mountain_valley = pd.merge(self.eda_df, mountain_valley, how='inner', on='contentId')

        lake_river = self.camp_thema()['lake_river'].iloc[:, :1]
        lake_river = pd.merge(self.eda_df, lake_river, how='inner', on='contentId')

        downtown = self.camp_thema()['downtown'].iloc[:, :1]
        downtown = pd.merge(self.eda_df, downtown, how='inner', on='contentId')

        return {'beach':beach, 'mountain_valley':mountain_valley, 'lake_river':lake_river, 'downtown':downtown}

    def reco_A500(self):
        ''' 1. 아이와함께 / 2. 여유롭게힐링 / 3. 체험액티비티 / 4. 투어,관광지,축제 '''

        kids_camp = self.purpose_camp()['kids_camp'].iloc[:, :1]
        kids_camp = pd.merge(self.eda_df, kids_camp, how='inner', on='contentId')

        healing_camp = self.purpose_camp()['healing_camp'].iloc[:, :1]
        healing_camp = pd.merge(self.eda_df, healing_camp, how='inner', on='contentId')

        field_trip = self.purpose_camp()['field_trip'].iloc[:, :1]
        field_trip = pd.merge(self.eda_df, field_trip, how='inner', on='contentId')

        tour_camp = self.purpose_camp()['tour_camp'].iloc[:, :1]
        tour_camp = pd.merge(self.eda_df, tour_camp, how='inner', on='contentId')


        return {'kids_camp':kids_camp, 'healing_camp':healing_camp, 'field_trip':field_trip, 'tour_camp':tour_camp}

    def reco_A600(self):
        ''' 1. 수도권 / 2. 동해,강원권 / 3. 남해,영남권 / 4. 서해,충청권 / 5. 호남권 / 6. 제주도 '''

        region_1 = self.region_camp()['region_1'].iloc[:, :1]
        region_1 = pd.merge(self.eda_df, region_1, how='inner', on='contentId')

        region_2 = self.region_camp()['region_2'].iloc[:, :1]
        region_2 = pd.merge(self.eda_df, region_2, how='inner', on='contentId')

        region_3 = self.region_camp()['region_3'].iloc[:, :1]
        region_3 = pd.merge(self.eda_df, region_3, how='inner', on='contentId')

        region_4 = self.region_camp()['region_4'].iloc[:, :1]
        region_4 = pd.merge(self.eda_df, region_4, how='inner', on='contentId')

        region_5 = self.region_camp()['region_5'].iloc[:, :1]
        region_5 = pd.merge(self.eda_df, region_5, how='inner', on='contentId')

        region_6 = self.region_camp()['region_6'].iloc[:, :1]
        region_6 = pd.merge(self.eda_df, region_6, how='inner', on='contentId')

        return {'region_1':region_1, 'region_2':region_2, 'region_3':region_3, 'region_4':region_4, 'region_5':region_5, 'region_6':region_6}


if __name__ == '__main__':
    df = UserWeights()
    print(df.reco_A600()['region_6'])
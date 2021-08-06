import pandas as pd
import re
from datetime import date
import config as config

class MainInsert:
    def __init__(self):
        self.camp=config.Config.CAMP
        self.festival=config.Config.FESTIVAL
        self.tour=config.Config.TOUR
        self.camp_details=config.Config.CAMP_DETAILS
        self.sigungu=config.Config.SIGUNGU

    # 캠핑장, 축제, 관광지 전처리
    def camping_data(self):
        camp = self.camp.drop(['allar', 'siteMg1Co', 'siteMg1Vrticl', 'siteMg1Width', 'siteMg2Co', 'siteMg2Vrticl', 
                'siteMg2Width', 'siteMg3Co', 'siteMg3Vrticl', 'siteMg3Width', 'zipcode', 'resveCl', 'resveUrl',
                'intro', 'direction', 'featureNm', 'hvofBgnde', 'hvofEnddle', 'tooltip'], 1)  
        festival = self.festival.drop(['areacode', 'cat1', 'cat2', 'cat3', 'contenttypeid', 'mlevel'], 1)
        tour = self.tour.drop(['areacode', 'booktour', 'cat1', 'cat2', 'cat3', 'contenttypeid', 'mlevel', 
                            'zipcode'], 1)
        camp = camp.rename(columns={'addr1' : 'addr',
                        'animalCmgCl' : 'animal_cmg',
                        'autoSiteCo' : 'auto_site',
                        'brazierCl' : 'brazier',
                        'caravAcmpnyAt' : 'carav_acmpny',
                        'caravSiteCo' : 'carav_site',
                        'clturEventAt' : 'clturevent_at',
                        'contentId' : 'content_id',
                        'createdtime' : 'created_date',
                        'exprnProgrmAt' : 'exprnprogrm_at',
                        'extshrCo' : 'extshr',
                        'facltNm' : 'place_name',
                        'fireSensorCo' : 'firesensor',
                        'frprvtSandCo' : 'frprvtsand',
                        'frprvtWrppCo' : 'frprvtwrpp',
                        'glampSiteCo' : 'glamp_site',
                        'gnrlSiteCo' : 'gnrl_site', 
                        'induty' : 'industry',
                        'indvdlCaravSiteCo' : 'indvdlcarav_site',
                        'insrncAt' : 'insrnc_at',
                        'manageNmpr' : 'manage_num',
                        'manageSttus' : 'manage_sttus',
                        'mangeDivNm' : 'mange',
                        'mapX' : 'lat', 
                        'mapY' : 'lng',                     
                        'modifiedtime' : 'modified_date',
                        'operDeCl' : 'oper_date',
                        'operPdCl' : 'oper_pd',
                        'prmisnDe' : 'prmisn_date',
                        'siteBottomCl1' : 'site_bottom1',
                        'siteBottomCl2' : 'site_bottom2',
                        'siteBottomCl3' : 'site_bottom3',
                        'siteBottomCl4' : 'site_bottom4',
                        'siteBottomCl5' : 'site_bottom5',
                        'sitedStnc' : 'sited_stnc',
                        'swrmCo' : 'swrm_cnt',
                        'toiletCo' : 'toilet_cnt',
                        'trlerAcmpnyAt' : 'trler_acmpny',
                        'wtrplCo' : 'wtrpl_cnt',
                        'clturEvent' : 'clturevent',
                        'eqpmnLendCl' : 'eqpmn_lend',
                        'firstImageUrl' : 'first_image',
                        'posblFcltyCl' : 'posblfclty',
                        'posblFcltyEtc' : 'posblfclty_etc',
                        'sbrsCl' : 'sbrs',
                        'sbrsEtc' : 'sbrs_etc', 
                        'themaEnvrnCl' : 'thema_envrn',
                        'tourEraCl' : 'tour_era',
                        'lctCl' : 'lct',
                        'facltDivNm' : 'faclt_div',
                        'lineIntro' : 'line_intro',
                        'trsagntNo' : 'trsagnt_no', 
                        'mgcDiv' : 'mgc_div',
                        'glampInnerFclty' : 'glampinner_fclty',
                        'caravInnerFclty' : 'caravinner_fclty',
                        'sigungucode' : 'sigungu_code',
                        'exprnProgrm' : 'exprnprogrm',
                        })
        camp['place_num'] = 0
        festival =festival.rename(columns={'addr1' : 'addr',
                                'contentid' : 'content_id',
                                'createdtime' : 'created_date',
                                'eventenddate' : 'event_end_date',
                                'eventstartdate' : 'event_start_date',
                                'firstimage' : 'first_image',
                                'firstimage2' : 'second_image',
                                'mapx' : 'lat',
                                'mapy' : 'lng',
                                'modifiedtime' : 'modified_date',
                                'sigungucode' : 'sigungu_code',
                                'title' : 'place_name'})
        festival['place_num'] = 1
        tour = tour.rename(columns={'addr1' : 'addr',
                            'contentid' : 'content_id',
                            'firstimage' : 'first_image',
                            'firstimage2' : 'second_image',
                            'mapx' : 'lat',
                            'mapy' : 'lng',
                            'sigungucode' : 'sigungu_code',
                            'title' : 'place_name'})
        tour['place_num'] = 2
        
        # 캠핑장 크롤링 데이터 전처리
        camp_details = self.camp_details.rename(columns={'view' : 'readcount'})
        camp_details['readcount'] = camp_details['readcount'].str.split(' ').str[1]
        datas = camp_details['link']
        data = [re.findall("\d+",data)[0] for data in datas]
        camp_details['url_num'] = data
        camp_details['url_num'] = camp_details['url_num'].astype('int')
        # 캠핑장 크롤링 과 API 데이터 merge
        final_data = pd.merge(camp, camp_details, how='right', left_on='content_id', right_on='url_num')
        return festival, tour, final_data
    
    # 캠핑장, 축제, 관광지 데이터 concat
    def concat_table(self, final_data, festival, tour):
        dataset = final_data.drop(['title', 'address'], 1)
        camp_festival = pd.concat([dataset, festival], 0)
        data = pd.concat([camp_festival, tour], 0)
        data = data.dropna(subset = ['addr'])
        data = data.reset_index()
        data.index = data.index + 1
        data['place_id'] = data.index
        data = data.drop(['index'],1)
        data = data.rename(columns={'img_url' : 'detail_image', 
                            'tags' : 'tag',
                            'view' : 'readcount', })
        # 캠핑장 관련 데이터만
        camp_df = data[data['place_num'] == 0]
        return data, camp_df

    # place table
    def place_table(self, data):
        place_df = data[['place_id', 'place_num', 'place_name', 'sigungu_code', 'addr', 'lat', 'lng', 'event_start_date', 
                        'event_end_date', 'first_image', 'second_image', 'tel', 'addr2', 'thema_envrn', 'tour_era', 
                        'homepage', 'line_intro', 'created_date', 'modified_date', 'detail_image', 'tag', 'readcount', 
                        'content_id', 'industry', 'oper_date', 'oper_pd',]]
        place_df = place_df.rename(columns={'place_id' : 'id'})
        return place_df

    # convenience table
    def convenience_table(self, camp_df):
        convenience_df = camp_df[['place_id','sited_stnc', 'brazier', 'site_bottom1', 'site_bottom2', 'site_bottom3', 
                                            'site_bottom4', 'site_bottom5', 'swrm_cnt', 'toilet_cnt', 'wtrpl_cnt', 'sbrs', 'sbrs_etc', 
                                            'eqpmn_lend']]
        return convenience_df

    # operation table
    def operation_table(self, camp_df):
        operation_df = camp_df[['place_id', 'mange', 'manage_sttus', 'prmisn_date', 'faclt_div', 'trsagnt_no', 
                                        'mgc_div', 'bizrno']]
        return operation_df
    
    # variety table
    def variety_table(self, camp_df):
        variety_df = camp_df[['place_id', 'glamp_site', 'gnrl_site', 'indvdlcarav_site', 'carav_site', 'auto_site', 
                                    'carav_acmpny', 'trler_acmpny', 'lct', 'animal_cmg', 'clturevent_at', 
                                    'exprnprogrm_at', 'clturevent', 'posblfclty', 'posblfclty_etc', 'glampinner_fclty', 
                                    'caravinner_fclty', 'exprnprogrm']]
        return variety_df
    
    # dafety table
    def safety_table(self, camp_df):
        safety_df = camp_df[['place_id', 'insrnc_at', 'manage_num', 'extshr', 'firesensor', 'frprvtsand', 'frprvtwrpp']]
        return safety_df
    
    # sigungu table
    def sigungu_table(self):
        sigungu_df = self.sigungu
        return sigungu_df

    
    







            


            


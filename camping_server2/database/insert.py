import pandas as pd
import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
# import MySQLdb
engine = create_engine("mysql+mysqldb://root:dss@34.136.89.21/camping")
conn = engine.connect()

from dbcamp import gocamp, naver
#place
api = pd.read_csv('./datas/camp_api_info_210613.csv')
festival = pd.read_csv('./datas/festival_210613.csv')
tour = pd.read_csv('./datas/tour_list_210612.csv')

place = pd.DataFrame(columns=[ 
                           'placeNum', 
                           'placeName', 
                           'sigungucode', 
                           'addr', 
                           'lat', 
                           'lng', 
                           'eventstartdate', 
                           'eventenddate',
                           'firstimage',
                           'firstimage2',
                           'tel',
                           'addr2',
                           'themaEnvrnCl', 
                           'tourEraCl',
                           'homepage',
                           'lineIntro',
                           'createdtime',
                           'modifiedtime',
                           'detailimage',
                           'tags',
                           'readcount', 
                          ])

api = api.drop(['Unnamed: 0', 'allar', 'contentId', 'siteMg1Co', 'siteMg1Vrticl', 'siteMg1Width', 'siteMg2Co', 
          'siteMg2Vrticl', 'siteMg2Width', 'siteMg3Co', 'siteMg3Vrticl', 'siteMg3Width', 'zipcode',
          'resveCl', 'resveUrl', 'intro', 'direction', 'featureNm', 'hvofBgnde', 'hvofEnddle', 'tooltip'], 1)  
festival = festival.drop(['Unnamed: 0', 'areacode', 'cat1', 'cat2', 'cat3', 'contentid', 'contenttypeid', 
               'mlevel', 'readcount'], 1)
tour = tour.drop(['Unnamed: 0', 'areacode', 'booktour', 'cat1', 'cat2', 'cat3', 'contentid',
                  'contenttypeid', 'mlevel', 'readcount', 'zipcode'], 1)

api.rename(columns={'addr1' : 'addr', 
                    'mapX' : 'lat', 
                    'mapY' : 'lng', 
                    'firstImageUrl' : 'firstimage',
                    'facltNm' : 'placeName'}, inplace=True)
api['placeNum'] = 0

festival.rename(columns={'addr1' : 'addr',
                         'mapx' : 'lat',
                         'mapy' : 'lng',
                         'title' : 'placeName'}, inplace=True)
festival['placeNum'] = 1

tour.rename(columns={'addr1' : 'addr',
                     'mapx' : 'lat',
                     'mapy' : 'lng',
                     'title' : 'placeName'}, inplace=True)
tour['placeNum'] = 2

file = pd.read_csv('./camp_details.csv')
final_data = gocamp(file)
place_a = pd.concat([place, final_data],0)
place_a.drop(['name', 'address'], 1, inplace=True)
place_b = pd.concat([place_a, festival], 0)
place_df = pd.concat([place_b, tour], 0)
place_df = place_df.reset_index().rename(columns={'level_0' : 'id'})
place_df.drop(['index'],1, inplace=True)
place_df.to_sql(name='place', con=engine, if_exists='replace', index=False)

#convenience
convenience_df = pd.DataFrame()
convenience_df = api[['sitedStnc', 'brazierCl', 'siteBottomCl1', 'siteBottomCl2', 'siteBottomCl3', 'siteBottomCl4', 'siteBottomCl5', 
    'swrmCo', 'toiletCo', 'wtrplCo', 'sbrsCl', 'sbrsEtc', 'eqpmnLendCl']]
convenience_df = convenience_df.reset_index().rename(columns={"index":"id"})
convenience_df.to_sql(name='convenience', con=engine, if_exists='replace', index=False)

#operation
operation_df = pd.DataFrame()
operation_df = api[['mangeDivNm', 'operDeCl', 'operPdCl', 'manageSttus', 'prmisnDe', 'facltDivNm', 'trsagntNo', 
                    'mgcDiv', 'bizrno']]
operation_df = operation_df.reset_index().rename(columns={"index":"id"})
operation_df.to_sql(name='operation', con=engine, if_exists='replace', index=False)

#variety
variety_df = pd.DataFrame()
variety_df = api[['induty', 'glampSiteCo', 'gnrlSiteCo', 'indvdlCaravSiteCo', 'caravSiteCo', 'autoSiteCo', 
                  'caravAcmpnyAt', 'trlerAcmpnyAt', 'lctCl', 'animalCmgCl', 'clturEventAt', 'exprnProgrmAt', 
                  'clturEvent', 'posblFcltyCl', 'posblFcltyEtc', 'glampInnerFclty', 'caravInnerFclty', 'exprnProgrm']]
variety_df = variety_df.reset_index().rename(columns={"index":"id"})
variety_df.to_sql(name='variety', con=engine, if_exists='replace', index=False)

#safety
safety_df = pd.DataFrame()
safety_df = api[['insrncAt', 'manageNmpr', 'extshrCo', 'fireSensorCo', 'frprvtSandCo', 'frprvtWrppCo']]
safety_df = safety_df.reset_index().rename(columns={"index":"id"})
safety_df.to_sql(name='safety', con=engine, if_exists='replace', index=False)

#review

file = pd.read_csv('./datas/v5_category_re.csv')
naver = naver(file)
review = pd.DataFrame(columns=['id', 
                           'platform', 
                           'userId', 
                           'placeId', 
                           'likeCnt', 
                           'photoCnt', 
                           'date', 
                           'tag', 
                           'star',
                           'content',
                          ])
review['photoCnt'] = naver['user_picture']
review['date'] = naver['visit_date']
review['tag'] = naver['category']
review['star'] = naver['star']
review['contents'] = naver['highlight_review']
review['platform'] = 1

kakao = pd.read_csv('.datas/kakao_camping_review_revised.csv')
kakao.rename(columns={'kakaoMapUserId':'userId', 'point' : 'star'}, inplace=True)
kakao['platform'] = 0
kakao_review = kakao[['platform', 'userId', 'likeCnt', 'photoCnt', 'date', 'star', 'contents']]
review_df = pd.concat([review, kakao_review], 0)
review_df.to_sql(name='review', con=engine, if_exists='replace', index=False)

#reviewer
reviewer = pd.DataFrame(columns=['id', 
                           'platform', 
                           'reviewId', 
                           'username', 
                           'meanStar', 
                           'visitCnt', 
                           'reviewCnt', 
                          ])
reviewer['username'] = kakao['username']
reviewer['platform'] = 0
reviewer.to_sql(name='reviewer', con=engine, if_exists='replace', index=False)
import pandas as pd
import re
from datetime import date

from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler, MaxAbsScaler

import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
import MySQLdb

ip = ""
db = ""
pw = ""
engine = create_engine(f"mysql+mysqldb://root:{pw}@{ip}/{db}]")
conn = engine.connect()

mydb = pymysql.connect(
    user = 'root',
    passwd = pw,
    host = ip,
    db = db,
    charset = 'utf8',
)
cursor = mydb.cursor(pymysql.cursors.DictCursor)

### dataset

api = pd.read_csv('/Users/sol/git/Algo_camping/camping_server2/scraping/datas/camp_api_info_210613.csv')
festival = pd.read_csv('/Users/sol/git/Algo_camping/camping_server2/scraping/datas/festival_210613.csv')
tour = pd.read_csv('/Users/sol/git/Algo_camping/camping_server2/scraping/datas/tour_list_210612.csv')
camp_details = pd.read_csv("/Users/sol/Desktop/dss/Crawling/camp_crawl_links.csv", encoding='utf-8-sig')

api = api.drop(['Unnamed: 0', 'allar', 'siteMg1Co', 'siteMg1Vrticl', 'siteMg1Width', 'siteMg2Co', 'siteMg2Vrticl', 
                'siteMg2Width', 'siteMg3Co', 'siteMg3Vrticl', 'siteMg3Width', 'zipcode', 'resveCl', 'resveUrl',
                'intro', 'direction', 'featureNm', 'hvofBgnde', 'hvofEnddle', 'tooltip'], 1)  
festival = festival.drop(['Unnamed: 0', 'areacode', 'cat1', 'cat2', 'cat3', 'contenttypeid', 'mlevel'], 1)
tour = tour.drop(['Unnamed: 0', 'areacode', 'booktour', 'cat1', 'cat2', 'cat3', 'contenttypeid', 'mlevel', 
                'zipcode'], 1)

api = api.rename(columns={'addr1' : 'addr',
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
api['place_num'] = 0
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

camp_details['view'] = camp_details['view'].str.split(' ').str[1]
camp_details.rename(columns={'view' : 'readcount'}, inplace=True)
datas = camp_details['link']
data = [re.findall("\d+",data)[0] for data in datas]
camp_details['url_num'] = data
camp_details['url_num'] = camp_details['url_num'].astype('int')
final_data = pd.merge(api, camp_details, how='right', left_on='content_id', right_on='url_num')

dataset = pd.DataFrame()
dataset_a = pd.concat([dataset, final_data],0)
dataset_a = dataset_a.drop(['title', 'address'], 1)
dataset_b = pd.concat([dataset_a, festival], 0)
data = pd.concat([dataset_b, tour], 0)
data = data.dropna(subset = ['addr'])
data = data.reset_index().reset_index()
data = data.drop(['index'],1)
data = data.rename(columns={'level_0' : 'place_id', 
                            'img_url' : 'detail_image', 
                            'tags' : 'tag',
                            'view' : 'readcount', 
                            })

### place
qry1 = ('''
CREATE TABLE place(
    id                INT            NOT NULL    AUTO_INCREMENT, 
    place_num         INT            NOT NULL    DEFAULT 0, 
    place_name        TEXT           NOT NULL, 
    sigungu_code      INT            NOT NULL, 
    addr              TEXT           NULL, 
    lat               FLOAT          NULL, 
    lng               FLOAT          NULL, 
    event_start_date  DATETIME       NULL, 
    event_end_date    DATETIME       NULL, 
    first_image       TEXT           NULL, 
    second_image      TEXT           NULL, 
    tel               TEXT           NULL, 
    addr2             VARCHAR(100)   NULL, 
    thema_envrn       VARCHAR(100)   NULL, 
    tour_era          VARCHAR(45)    NULL, 
    homepage          TEXT           NULL, 
    line_intro        TEXT           NULL, 
    created_date      DATETIME       NULL, 
    modified_date     DATETIME       NULL, 
    detail_image      TEXT           NULL, 
    tag               TEXT           NULL, 
    readcount         INT            NULL, 
    content_id        INT            NOT NULL   UNIQUE, 
    industry          VARCHAR(45)    NULL, 
    oper_date         VARCHAR(45)    NULL, 
    oper_pd           VARCHAR(45)    NULL, 
    CONSTRAINT PK_place PRIMARY KEY (id, sigungu_code, content_id)
);

''')

cursor.execute(qry1)

place_df = data[['place_id', 'place_num', 'place_name', 'sigungu_code', 'addr', 'lat', 'lng', 'event_start_date', 
                'event_end_date', 'first_image', 'second_image', 'tel', 'addr2', 'thema_envrn', 'tour_era', 
                'homepage', 'line_intro', 'created_date', 'modified_date', 'detail_image', 'tag', 'readcount', 
                'content_id', 'industry', 'oper_date', 'oper_pd',]]
place_df = place_df.rename(columns={'place_id' : 'id'})

place_df.to_sql(name='place', con=engine, if_exists='append', index=False)

### convenience
qry2 = ('''
CREATE TABLE convenience(
    id                INT            NOT NULL    AUTO_INCREMENT, 
    place_id          INT            NOT NULL,
    sited_stnc    INT            NULL    , 
    brazier       VARCHAR(45)    NULL    , 
    site_bottom1  INT            NULL    , 
    site_bottom2  INT            NULL    , 
    site_bottom3  INT            NULL    , 
    site_bottom4  INT            NULL    , 
    site_bottom5  INT            NULL    , 
    swrm_cnt      INT            NULL    , 
    toilet_cnt    INT            NULL    , 
    wtrpl_cnt     INT            NULL    , 
    sbrs          TEXT           NULL    , 
    sbrs_etc      TEXT           NULL    , 
    eqpmn_lend    VARCHAR(45)    NULL    , 
    CONSTRAINT PK_편리성 PRIMARY KEY (id)
);
''')
cursor.execute(qry2)

camp_convenience_df = data[data['place_num'] == 0]
convenience_df = camp_convenience_df[['place_id','sited_stnc', 'brazier', 'site_bottom1', 'site_bottom2', 'site_bottom3', 
                                        'site_bottom4', 'site_bottom5', 'swrm_cnt', 'toilet_cnt', 'wtrpl_cnt', 'sbrs', 'sbrs_etc', 
                                        'eqpmn_lend']]

convenience_df.to_sql(name='convenience', con=engine, if_exists='append', index=False)

qry3 = ('''
SET foreign_key_checks = 0;
''')
cursor.execute(qry3)

qry4 = ('''
ALTER TABLE convenience
    ADD CONSTRAINT FK_convenience_id_place_id FOREIGN KEY (place_id)
        REFERENCES place (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
        ''')
cursor.execute(qry4)

qry5 = ('''
SET foreign_key_checks = 1;
''')
cursor.execute(qry5)

### operation
qry6 = ('''
CREATE TABLE operation(
    id                INT            NOT NULL    AUTO_INCREMENT, 
    place_id          INT            NOT NULL, 
    mange         VARCHAR(45) , 
    manage_sttus  VARCHAR(45) , 
    prmisn_date   DATETIME    , 
    faclt_div     VARCHAR(45) , 
    trsagnt_no    VARCHAR(45) , 
    mgc_div       VARCHAR(45) , 
    bizrno        VARCHAR(45) , 
    CONSTRAINT PK_운영 PRIMARY KEY (id)
);
''')
cursor.execute(qry6)

camp_operation_df = data[data['place_num'] == 0]
operation_df = camp_operation_df[['place_id', 'mange', 'manage_sttus', 'prmisn_date', 'faclt_div', 'trsagnt_no', 
                                'mgc_div', 'bizrno']]

operation_df.to_sql(name='operation', con=engine, if_exists='append', index=False)

qry7 = ('''
SET foreign_key_checks = 0;
''')
cursor.execute(qry7)

qry8 = ('''
ALTER TABLE operation
    ADD CONSTRAINT FK_operation_id_place_id FOREIGN KEY (place_id)
        REFERENCES place (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
        ''')
cursor.execute(qry8)

qry9 = ('''
SET foreign_key_checks = 1;
''')
cursor.execute(qry9)

### variety
qry10 = ('''
CREATE TABLE variety(
    id                INT            NOT NULL    AUTO_INCREMENT, 
    place_id          INT            NOT NULL,
    glamp_site        INT            , 
    gnrl_site         INT            , 
    indvdlcarav_site  INT            , 
    carav_site        INT            , 
    auto_site         INT            , 
    carav_acmpny      VARCHAR(45)    , 
    trler_acmpny      VARCHAR(45)    , 
    lct               VARCHAR(45)    , 
    animal_cmg        VARCHAR(45)    , 
    clturevent_at     TEXT           , 
    exprnprogrm_at    TEXT    , 
    clturevent        TEXT    , 
    posblfclty        TEXT           , 
    posblfclty_etc    TEXT           , 
    glampinner_fclty  VARCHAR(45)    , 
    caravinner_fclty  VARCHAR(45)    , 
    exprnprogrm       TEXT          , 
    CONSTRAINT PK_다양성 PRIMARY KEY (id)
);
''')
cursor.execute(qry10)

camp_variety_df = data[data['place_num'] == 0]
variety_df = camp_variety_df[['place_id', 'glamp_site', 'gnrl_site', 'indvdlcarav_site', 'carav_site', 'auto_site', 
                                'carav_acmpny', 'trler_acmpny', 'lct', 'animal_cmg', 'clturevent_at', 
                                'exprnprogrm_at', 'clturevent', 'posblfclty', 'posblfclty_etc', 'glampinner_fclty', 
                                'caravinner_fclty', 'exprnprogrm']]

variety_df.to_sql(name='variety', con=engine, if_exists='append', index=False)

qry11 = ('''
SET foreign_key_checks = 0;
''')
cursor.execute(qry11)

qry12 = ('''
ALTER TABLE variety
    ADD CONSTRAINT FK_variety_id_place_id FOREIGN KEY (place_id)
        REFERENCES place (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
''')
cursor.execute(qry12)

qry13 = ('''
SET foreign_key_checks = 1;
''')
cursor.execute(qry13)

### safety
qry14 = ('''
CREATE TABLE safety(
    id                INT            NOT NULL    AUTO_INCREMENT, 
    place_id          INT            NOT NULL, 
    insrnc_at   VARCHAR(45)    , 
    manage_num  INT            , 
    extshr      INT            , 
    firesensor  INT            , 
    frprvtsand  INT            , 
    frprvtwrpp  INT            , 
    CONSTRAINT PK_안전성 PRIMARY KEY (id)
);
''')
cursor.execute(qry14)

camp_safety_df = data[data['place_num'] == 0]
safety_df = camp_safety_df[['place_id', 'insrnc_at', 'manage_num', 'extshr', 'firesensor', 'frprvtsand', 'frprvtwrpp']]


safety_df.to_sql(name='safety', con=engine, if_exists='append', index=False)

qry15 = ('''
SET foreign_key_checks = 0;
''')
cursor.execute(qry15)

qry16 = ('''
ALTER TABLE safety
    ADD CONSTRAINT FK_safety_id_place_id FOREIGN KEY (place_id)
        REFERENCES place (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
''') 
cursor.execute(qry16)

qry17 = ('''
SET foreign_key_checks = 1;
''')
cursor.execute(qry17)


### review_dataset
# naver
naver = pd.read_csv('/Users/sol/git/Algo_camping/camping_server2/scraping/datas/v5_category_re.csv')
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

# kakao
kakao = pd.read_csv('/Users/sol/Desktop/dss/Crawling/data/kakao_camping_review_revised.csv')
kakao = kakao.rename(columns={'kakaoMapUserId' : 'user_id', 'point' : 'star', 'likeCnt' : 'like_cnt', 
                        'photoCnt' : 'photo_cnt', 'username' : 'user_nickname'})
kakao['platform'] = 0
kakao_naver = pd.concat([naver, kakao], 0)
review_data = data[['place_id', 'place_name']]
review_data_df = pd.merge(review_data, kakao_naver, left_on='place_name', right_on='place_name', how="right")
review_data_df = review_data_df.drop_duplicates()
review_data_df = review_data_df.reset_index()
review_data_df = review_data_df.rename(columns={'index' : 'id', 'userId' : 'user_id', })
### review

qry18 = ('''
CREATE TABLE review(
    id INT PRIMARY KEY AUTO_INCREMENT,
    platform INT NOT NULL DEFAULT 0, 
    user_id VARCHAR(45), 
    place_id INT NOT NULL, 
    like_cnt INT, 
    photo_cnt INT, 
    date DATETIME, 
    cat_tag VARCHAR(45), 
    star FLOAT, 
    contents TEXT 
);
''')
cursor.execute(qry18)

review_df = review_data_df[['platform', 'user_id', 'place_id', 'like_cnt', 'photo_cnt', 'date', 'cat_tag', 
                            'star', 'contents']]
review_df = review_df.dropna(subset = ['place_id'])
review_df.to_sql(name='review', con=engine, if_exists='append', index=False)

qry19 = ('''
SET foreign_key_checks = 0;
''')
cursor.execute(qry19)

qry20 = ('''
ALTER TABLE review
    ADD CONSTRAINT FK_review_place_id_place_id FOREIGN KEY (place_id)
        REFERENCES place (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
''')
cursor.execute(qry20)

qry21 = ('''
SET foreign_key_checks = 1;
''')
cursor.execute(qry21)

### reviewer
qry22 = ('''
CREATE TABLE reviewer(
    id             INT            NOT NULL       AUTO_INCREMENT, 
    platform       INT            NOT NULL       DEFAULT 0, 
    review_id      INT            NOT NULL       , 
    user_nickname  VARCHAR(45)    , 
    mean_star      FLOAT         , 
    visit_cnt      INT            , 
    review_cnt     INT            , 
    CONSTRAINT PK_reviewer PRIMARY KEY (id)
);
''')
cursor.execute(qry22)

reviewer = review_data_df[['id', 'platform', 'user_nickname', 'mean_star', 'visit_cnt', 'review_cnt']]
reviewer_df = reviewer.rename(columns={'id' : 'review_id'})
reviewer_df['visit_cnt'] = reviewer_df['visit_cnt'].str.split('').str[1] # 나중에 정규표현식으로 수정
reviewer_df.to_sql(name='reviewer', con=engine, if_exists='append', index=False)

qry23 = ('''
SET foreign_key_checks = 0;
''')
cursor.execute(qry23)

qry24 = ('''
ALTER TABLE reviewer
    ADD CONSTRAINT FK_reviewer_review_id_review_id FOREIGN KEY (review_id)
        REFERENCES review (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
''')
cursor.execute(qry24)

qry25 = ('''
SET foreign_key_checks = 1;
''')
cursor.execute(qry25)

### search
qry26 = ('''
CREATE TABLE search(
    id             INT           NOT NULL        AUTO_INCREMENT, 
    content_id     INT           NOT NULL        UNIQUE, 
    place_name     TEXT   NOT NULL, 
    addr           TEXT   NOT NULL, 
    tag            TEXT                , 
    with_family_s  INT                 , 
    valley_s       INT                , 
    clean_s        INT               , 
    trail_s        INT              , 
    cultural_s     INT              , 
    waterplay_s    INT            , 
    pure_water_s   INT            , 
    ocean_s        INT           , 
    with_pet_s     INT            , 
    star_s         INT            , 
    spacious_s     INT            , 
    ecological_s   INT            , 
    pool_s         INT            , 
    with_child_s   INT            , 
    hot_water_s    INT            , 
    extreme_s      INT            , 
    bicycle_s      INT            , 
    parking_s      INT            , 
    festival_s     INT            , 
    with_couple_s  INT            , 
    healing_s      INT            , 
    activity_m     INT            , 
    nature_m       INT            , 
    fun_m          INT            , 
    comfort_m      INT            , 
    together_m     INT            , 
    CONSTRAINT PK_modeling PRIMARY KEY (id)
);
''')
cursor.execute(qry26)

camping_data = data[data['place_num'] == 0]
camping_data = data[['place_id', 'content_id', 'place_name', 'addr', 'tag', 'animal_cmg']]
camping_data['tag'] = camping_data['tag'].fillna("")
camping_data["tag"][camping_data["animal_cmg"] == "가능"] = camping_data[camping_data["animal_cmg"] == "가능"]["tag"] + "#반려견"
camping_data["tag"][camping_data["animal_cmg"] == "가능(소형견)"] = camping_data[camping_data["animal_cmg"] == "가능(소형견)"]["tag"] + "#반려견"

lookup = pd.read_csv("/Users/sol/Downloads/3.csv")
lookup.columns = ["sub_cat", "main_cat"]
lookup['sub_cat'] = lookup['sub_cat'].str.replace(" ","")
lookup['main_cat'] = lookup['main_cat'].str.replace(" ","")
camping_data['tag'] = [t[:] if type(t) == str else "" for t in camping_data['tag']]

for kw in ['#봄 ', '#여름 ', '#가을', '#가을 ', '#겨울', '봄 ', '여름 ', '가을 ', '겨울',]:
    camping_data['tag'] = [t.replace(kw, "") if type(t) == str else "" for t in camping_data['tag']]

camping_data["tag"] = camping_data["tag"].str.replace(" ", "")
camping_data_a = camping_data["tag"].str.split("#").apply(pd.Series).loc[:, 1:]
camping_data_b = pd.get_dummies(camping_data_a.stack()).reset_index().groupby("level_0").sum().drop("level_1", 1)
main_df = pd.DataFrame()

for i in range(len(camping_data_b)):
    main_df = pd.concat([pd.DataFrame(camping_data_b.values[i] * lookup["main_cat"].T), main_df], 1)

main_df = main_df.T.reset_index(drop=True)
main_df = pd.get_dummies(main_df.stack()).reset_index().groupby("level_0").sum().drop("level_1", 1)
main_df = main_df.iloc[:,1:]
main_df.index = camping_data_b.index
last_df  = pd.concat([camping_data_b, main_df], 1)
last_df[last_df > 1] = 1
last_df['index']= last_df.index
algo_search_df = pd.merge(camping_data, last_df, how="left", left_on = 'place_id', right_on='index').drop("index", 1)
algo_search_df = algo_search_df.rename(columns={'가족' : 'with_family_s',
                                    '계곡옆' : 'valley_s',
                                    '깨끗한' : 'clean_s',
                                    '둘레길' : 'trail_s',
                                    '문화유적' : 'cultural_s',
                                    '물놀이하기좋은' : 'waterplay_s',
                                    '물맑은' : 'pure_water_s',
                                    '바다가보이는' : 'ocean_s',
                                    '반려견' : 'with_pet_s',
                                    '별보기좋은' : 'star_s',
                                    '사이트간격이넓은' : 'spacious_s',
                                    '생태교육' : 'ecological_s',
                                    '수영장있는' : 'pool_s',
                                    '아이들놀기좋은' : 'with_child_s',
                                    '온수잘나오는' : 'hot_water_s',
                                    '익스트림' : 'extreme_s',
                                    '자전거타기좋은' : 'bicycle_s',
                                    '차대기편한' : 'parking_s',
                                    '축제' : 'festival_s',
                                    '커플' : 'with_couple_s', 
                                    '힐링' : 'healing_s',
                                    '액티비티' : 'activity_m',
                                    '자연/힐링' : 'nature_m',
                                    '즐길거리' : 'fun_m',
                                    '쾌적/편리' : 'comfort_m',
                                    '함께' : 'together_m'})

search_df = algo_search_df.drop(['place_id','animal_cmg', '재미있는', '친절한', '여유있는', '그늘이많은'],1)
search_df.to_sql(name='search', con=engine, if_exists='append', index=False)

qry27 = ('''
SET foreign_key_checks = 0;
''')
cursor.execute(qry27)

qry28 = ('''
ALTER TABLE search
    ADD CONSTRAINT FK_search_content_id_place_content_id FOREIGN KEY (content_id)
        REFERENCES place (content_id) ON DELETE RESTRICT ON UPDATE RESTRICT;
''')
cursor.execute(qry28)

qry29 = ('''
SET foreign_key_checks = 1;
''')
cursor.execute(qry29)

### congestion

qry30 = ('''
CREATE TABLE congestion(
    id            INT         NOT NULL        AUTO_INCREMENT, 
    sigungu_code  INT         NOT NULL, 
    base_ymd      DATETIME    NOT NULL, 
    created_date  DATETIME    NOT NULL, 
    congestion    FLOAT       NOT NULL, 
    content_id    INT         NOT NULL        UNIQUE, 
    CONSTRAINT PK_congestion PRIMARY KEY (id)
);
''')
cursor.execute(qry30)

visitor_api = pd.read_csv('locgo_visitor_api_info1.csv')
visitor_api = visitor_api.rename(columns={'signguCode' : 'sigungu_code'})
visitor_api_df = visitor_api.groupby(['sigungu_code', 'baseYmd']).sum()
visitor_api_df = visitor_api_df.reset_index()
camping_data = data[data['place_num'] == 0]
visitor_api_merge = pd.merge(visitor_api_df, camping_data, how='left', on='sigungu_code')
esti_api = pd.read_csv('/Users/sol/Desktop/dss/Crawling/tour_estiDeco_api_info.csv')
esti_api_df = pd.merge(esti_api, data, how='left', left_on='contentId', right_on='content_id')
future = esti_api_df[['baseYmd', 'estiNum', 'content_id', 'sigungu_code']]
future_df = future.groupby(['sigungu_code', 'baseYmd']).sum()
future_df = future_df.reset_index()
future_api = pd.merge(future_df, future, how='left', on = ['sigungu_code', 'baseYmd'])
future_api = future_api.drop(['content_id_x', 'estiNum_y'],1)
past_api = visitor_api_merge[['sigungu_code', 'baseYmd', 'touNum', 'content_id']]
past_api = past_api.dropna()
future_api = future_api.rename(columns={'baseYmd' : 'base_ymd',
                  'estiNum_x' : 'congestion',
                'content_id_y' : 'content_id'})

past_api = past_api.rename(columns={'baseYmd' : 'base_ymd',
                     'touNum' : 'congestion'})
con_df = pd.concat([past_api,future_api])
congestion_df = con_df.reset_index()
congestion_df = congestion_df.drop(['index'],1)

today = date.today()
today.isoformat()
congestion_df['created_date'] = today.isoformat()
congestion_df = congestion_df.rename(columns={'index' : 'id', 'baseYmd' : 'base_ymd', 
                              'touNum' : 'congestion'})
congestion_df = congestion_df.dropna()

congestion_df.to_sql(name='congestion', con=engine, if_exists='append', index=False)

qry31 = ('''
SET foreign_key_checks = 0;
''')
cursor.execute(qry31)

qry31 = ('''
ALTER TABLE congestion
    ADD CONSTRAINT FK_congestion_sigungu_code_place_sigungu_code FOREIGN KEY (sigungu_code)
        REFERENCES place (sigungu_code) ON DELETE RESTRICT ON UPDATE RESTRICT;
''')
cursor.execute(qry31)

qry32 = ('''
SET foreign_key_checks = 1;
''')
cursor.execute(qry32)

# algorithm
qry40 = ((('''
CREATE TABLE algorithm(
    id                INT            NOT NULL    AUTO_INCREMENT, 
    place_name        TEXT           NULL, 
    place_id          INT            NOT NULL, 
    content_id        INT            NULL, 
    insrnc_at         VARCHAR(45)    NULL, 
    trsagnt_no        VARCHAR(45)    NULL, 
    mange             VARCHAR(45)    NULL, 
    manage_num        INT            NULL, 
    sited_stnc        INT            NULL, 
    glampinner_fclty  INT            NULL, 
    caravinner_fclty  INT            NULL, 
    trler_acmpny      VARCHAR(45)    NULL, 
    carav_acmpny      VARCHAR(45)    NULL, 
    toilet_cnt        INT            NULL, 
    swrm_cnt          INT            NULL, 
    wtrpl_cnt         INT            NULL, 
    brazier           VARCHAR(45)    NULL, 
    sbrs              INT            NULL, 
    sbrs_etc          INT            NULL, 
    posblfclty        INT            NULL, 
    extshr            INT            NULL, 
    frprvtwrpp        INT            NULL, 
    frprvtsand        INT            NULL, 
    firesensor        INT            NULL, 
    animal_cmg        VARCHAR(45)    NULL, 
    spacious_s        INT            NULL, 
    clean_s           INT            NULL, 
    hot_water_s       INT            NULL, 
    parking_s         INT            NULL, 
    with_child_s      INT            NULL, 
    ecological_s      INT            NULL, 
    cultural_s        INT            NULL, 
    festival_s        INT            NULL, 
    trail_s           INT            NULL, 
    bicycle_s         INT            NULL, 
    star_s            INT            NULL, 
    healing_s         INT            NULL, 
    with_couple_s     INT            NULL, 
    with_family_s     INT            NULL, 
    pool_s            INT            NULL, 
    valley_s          INT            NULL, 
    waterplay_s       INT            NULL, 
    pure_water_s      INT            NULL, 
    shade_s           INT            NULL, 
    ocean_s           INT            NULL, 
    extreme_s         INT            NULL, 
    price_r           INT            NULL, 
    satisfied_r       INT            NULL, 
    taste_r           INT            NULL, 
    main_r            INT            NULL, 
    object_r          INT            NULL, 
    facility_r        INT            NULL, 
    atmos_r           INT            NULL, 
    equipment_r       INT            NULL, 
    service_r         INT            NULL, 
    pool_r            INT            NULL, 
    manage_r          INT            NULL, 
    childlike_r       INT            NULL, 
    reservation_r     INT            NULL, 
    wifi_r            INT            NULL, 
    location_r        INT            NULL, 
    food_r            INT            NULL, 
    enter_r           INT            NULL, 
    view_r            INT            NULL, 
    parking_r         INT            NULL, 
    exciting_r        INT            NULL, 
    clean_r           INT            NULL, 
    conv_facility_r   INT            NULL, 
    congestion_r      INT            NULL, 
     PRIMARY KEY (id)
);
''')))

cursor.execute(qry40)

camping_data = data[data['place_num'] == 0]
tmp = camping_data[['content_id', 'insrnc_at', 'trsagnt_no', 'mange', 'manage_num', 'sited_stnc', 'glampinner_fclty', 'caravinner_fclty', 'trler_acmpny', 'carav_acmpny', 'toilet_cnt', 'swrm_cnt', 'wtrpl_cnt', 'brazier', 'sbrs', 'sbrs_etc', 'posblfclty', 'extshr', 'frprvtwrpp', 'frprvtsand', 'firesensor',]]
tmp_df = pd.merge(algo_search_df, tmp, how='left', on='content_id')
def col_count(colname):
    tmp_df[f'{colname}'] = tmp_df[f'{colname}'].str.count(',') + 1
    tmp_df[f'{colname}'] = tmp_df[f'{colname}'].fillna(0)
    tmp_df[f'{colname}'] = tmp_df[f'{colname}'].astype('int')

col_list = ['glampinner_fclty', 'caravinner_fclty', 'sbrs', 'sbrs_etc', 'posblfclty']
for i in col_list:
    col_count(i)
nv_data = pd.read_csv('/Users/sol/git/Algo_camping/camping_server2/scraping/datas/v5_category_re.csv')
kk_data = pd.read_csv('/Users/sol/Desktop/dss/Crawling/data/kakao_camping_review_revised.csv')
nv_data['user_info'] = nv_data['user_info'].fillna(0)
nv_data = nv_data[nv_data['user_info'] != 0]
nv_data['user_info'] = nv_data['user_info'].apply(lambda x: x.split('\n')[-1])
nv_data['visit_info'] = nv_data['visit_info'].apply(lambda x: x.split('번째')[0][-1])
nv_data = nv_data[nv_data['star'] != 'star']

nv_data['star'] = nv_data['star'].astype('float64')
nv_data['user_info'] = nv_data['user_info'].astype('float64')
nv_data['visit_info'] = nv_data['visit_info'].astype('float64')
nv_data = nv_data.drop(['addr', 'base_addr', 'user_name', 'visit_info'], 1)
nv_data = nv_data.rename(
    columns={'title': 'camp', 'highlight_review': 'review', 'star': 'point', 'user_info': 'avg_point'})

nv_data = nv_data[['camp', 'review', 'point', 'category', 'avg_point']]
nv_data['point'] = nv_data['point'].astype('float64')
nv_data['avg_point'] = nv_data['avg_point'].astype('float64')

reviews_df = pd.concat([nv_data, kk_data], 0)
# 가중치 [ point / (point / avg_point) ] * 0.01 → RobustScaler 적용
reviews_df['weights'] = reviews_df['point'] * (reviews_df['point'] / reviews_df['avg_point'])
reviews_df = reviews_df.reset_index(drop=True)

rb = RobustScaler()
rb_df = rb.fit_transform(reviews_df[['weights']])
rb_df = pd.DataFrame(rb_df)

rb_df = rb_df.rename(columns={0: 'weights2'})
rb_df['weights2'] = rb_df['weights2'] * 0.01

re_df = pd.concat([reviews_df, rb_df], 1)

# final_point: point * (1+weights) → MinMaxScaler 적용 후 *5 (0~5 사이의 값)

re_df['final_point'] = re_df['point'] * (1 + re_df['weights2'])

mm = MinMaxScaler()
mm_df = mm.fit_transform(re_df[['final_point']])
mm_df = pd.DataFrame(mm_df)

re_df['final_point'] = mm_df * 5
re_df = re_df.drop(['weights', 'weights2'], 1)
re_df['final_point'] = round(re_df['final_point'], 1)

re_df2 = re_df.groupby(['camp', 'category']).mean().reset_index()
re_df3 = re_df.groupby(['camp', 'category']).size().reset_index(name='count')
re_df4 = pd.merge(re_df2, re_df3)

df = re_df4[['camp', 'category', 'final_point']]
df = pd.pivot_table(df, index='camp', columns='category')
df = df.fillna(0)
df = df.reset_index()
review_result = pd.concat([df["camp"], df["final_point"]], 1)

camp_name = ['느티나무 캠핑장', '늘푸른캠핑장', '두리캠핑장', '둥지캠핑장', '백운계곡캠핑장', '별빛야영장',
             '별헤는 밤', '산여울캠핑장', '소풍캠핑장', '솔바람 캠핑장', '솔밭야영장', '솔밭캠핑장', '포시즌',
             '포시즌 캠핑장']

for i in camp_name:
    review_result = review_result.query(f'camp != "{i}"')

merge_result = pd.merge(api, review_result, how='outer', left_on='place_name', right_on='camp')

result1 = merge_result.iloc[:, 44:].fillna(0)
result2 = merge_result.iloc[:, :44]
algo_result = pd.concat([result2, result1], 1)
algo_result = algo_result[['content_id', '가격', '만족도',
       '맛', '메인시설', '목적', '부대/공용시설', '분위기', '비품', '서비스', '수영장', '시설물관리',
       '아이 만족도', '예약', '와이파이', '위치', '음식/조식', '입장', '전망', '주차', '즐길거리',
       '청결도', '편의/부대시설', '혼잡도']]
algo_df = pd.merge(tmp_df, algo_result, how='left', on='content_id')
algo_df = algo_df.rename(columns={'id' : 'place_id',
                       '그늘이많은' : 'shade_s',
                       '가격' : 'price_r',
                       '만족도' : 'satisfied_r', 
                        '맛' : 'taste_r',
                        '메인시설' : 'main_r', 
                        '목적' : 'object_r', 
                        '부대/공용시설' : 'facility_r', 
                        '분위기' : 'atmos_r', 
                        '비품' : 'equipment_r', 
                        '서비스' : 'service_r', 
                        '수영장' : 'pool_r', 
                        '시설물관리' : 'manage_r', 
                        '아이 만족도' : 'childlike_r',
                        '예약' : 'reservation_r', 
                        '와이파이' : 'wifi_r', 
                        '위치' : 'location_r', 
                        '음식/조식' : 'food_r', 
                        '입장' : 'enter_r', 
                        '전망' : 'view_r', 
                        '주차' : 'parking_r', 
                        '즐길거리' : 'exciting_r', 
                        '청결도' : 'clean_r', 
                        '편의/부대시설' : 'conv_facility_r',
                        '혼잡도' : 'congestion_r'})
algo_df = algo_df.drop(['addr', 'tag', '여유있는', '재미있는', '친절한', 'activity_m', 'nature_m', 'fun_m', 'comfort_m', 'together_m', 'with_pet_s' ],1)
algo_df.to_sql(name='algorithm', con=engine, if_exists='append', index=False)

qry41 = ('''
SET foreign_key_checks = 0;
''')
cursor.execute(qry41)

qry42 = ('''
ALTER TABLE algorithm
    ADD CONSTRAINT FK_algorithm_place_id_place_id FOREIGN KEY (place_id)
        REFERENCES place (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
''')
cursor.execute(qry42)

qry43 = ('''
SET foreign_key_checks = 1;
''')
cursor.execute(qry43)






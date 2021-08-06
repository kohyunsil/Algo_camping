from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import xmltodict
import json
from pandas.io.json import json_normalize
import pandas as pd
import re
import datetime
# from datetime import datetime
import pymysql
from sqlalchemy import create_engine

pymysql.install_as_MySQLdb()
# import camping_server2.config as config

class Gocamp:
    base_url = "https://www.gocamping.or.kr"
    path = "/bsite/camp/info/list.do"
    query = "?pageUnit=3000&searchKrwd=&listOrdrTrget=last_updusr_pnttm"
    url = base_url + path + query

    def __init__(self):
        self.secretKey = "1lQh1AXwuKpBPamJ8M10NbN0c0hg%2Beex7NUu6k5HgjiP%2FupWExgtLRbmjRV7XLAEMf5l0j%2FH5um7uy4Z0cErXg%3D%3D"

    # gocamp API
    def gocampingAPI(self):
        url = 'http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?'
        param = 'ServiceKey='+self.secretKey+'&MobileOS=ETC&MobileApp=AppTest&numOfRows=3000'

        request = Request(url+param)
        request.get_method = lambda: 'GET'
        response = urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            responseData = response.read()
            rD = xmltodict.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)

            camp_api_df = json_normalize(rDD['response']['body']['items']['item'])
            return camp_api_df

    # gocamp crawling
    def detail_page(self, content_id):
        base_url = f"https://www.gocamping.or.kr/bsite/camp/info/read.do?c_no={content_id}&viewType=read01&listOrdrTrget=last_updusr_pnttm"
        response = requests.get(base_url)
        dom = BeautifulSoup(response.content, 'html.parser')

        param = {'title': '', 'tags': '', 'address': '', 'img_url': ''}

        param['title'] = dom.select_one('#sub_title_wrap2 > div.layout > div.s_title2 > p.camp_name').text.strip().split('\n')[0]
        param['tags'] = dom.select_one('div.camp_tag > ul.tag_list').text.strip().replace('\n', ' ')
        param['address'] = dom.select_one('#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-of-type(1) > td').text

        imgs = dom.select('#contents > div > div.layout > div > div > div > a > img')
        img_list = []
        for img in imgs:
            img_list.append(img['src'])
        param['img_url'] = img_list

        return param


    # readcount를 가져오기 위한 검색결과 페이지 정보 가져오기
    def search_page(self, place_name):
        base_url = f"https://www.gocamping.or.kr/bsite/camp/info/list.do?searchKrwd={place_name}"
        response = requests.get(base_url)
        dom = BeautifulSoup(response.content, 'html.parser')

        param = {'title': '', 'address': '', 'readcount': ''}

        search_list = dom.select("#cont_inner > div > div.camp_search_list > ul > li")
        try:
            place_name = search_list[0].select_one("h2 > a").text.split('] ')[1]
            addr = search_list[0].select_one(".addr").text
            read_count = search_list[0].select_one('div > div > p > span.item_t03').text
        except:
            place_name, addr, read_count = '', '', ''

        param['title'] = place_name
        param['address'] = addr
        param['readcount'] = read_count

        return param
    # 자동화 실행 날기준으로 새롭게 업데이트된 정보만 가져옴
    def update_date(self, data):
        diff_days = datetime.timedelta(days=7)
        today = datetime.date.today()
        last_day = today - diff_days
        last_day = last_day.isoformat().replace("-","")

        data['createdtime'] = data['createdtime'].str.replace("-","")
        data['createdtime2'] = data['createdtime'].apply(lambda x: x[:8])
        new_data = data[data['createdtime2'] >= last_day]
        new_data = new_data.drop(["createdtime"],1)
        new_data = new_data.rename(columns={'createdtime2' : 'createdtime'})
        return new_data
    # gocamp API 전처리
    def make_camp_api(self, camp_api_df):
        camp = camp_api_df.drop(['allar', 'siteMg1Co', 'siteMg1Vrticl', 'siteMg1Width', 'siteMg2Co', 'siteMg2Vrticl',
                'siteMg2Width', 'siteMg3Co', 'siteMg3Vrticl', 'siteMg3Width', 'zipcode', 'resveCl', 'resveUrl',
                'intro', 'direction', 'featureNm', 'hvofBgnde', 'hvofEnddle', 'tooltip'], 1)
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
        return camp
    # gocamp crawling 코드 실행 및 하나의 데이터로 merge
    def make_camp_crawling(self, new_data) :
        content_id = list(new_data['contentId'])
        content_id = list(map(int, content_id))
        place_name = list(new_data['facltNm'])

        details = []
        search = []

        # gocamp crawling
        # 상세 페이지 place_name, addr, tag, detail_image 크롤링 (content_id 기준)
        for c_id in content_id:
            new_details = gocamp.detail_page(c_id)
            details.append(new_details)

        data_details = pd.DataFrame(details)

        # 검색 페이지 place_name, addr, read_count 크롤링 (place_name 기준)
        for name in place_name:
            new_search = gocamp.search_page(name.replace(' ', ''))
            search.append(new_search)
        data_search = pd.DataFrame.from_dict(search)
        data_search = data_search.drop(['title'],1)

        # merge
        camp_details = pd.merge(data_details, data_search, how='left', on='address')
        camp_details['img_url'] = camp_details['img_url'].apply(pd.Series)
        camp_details['url_num'] = content_id
        camp_details['url_num'] = camp_details['url_num'].astype(str)

        camp_details['readcount'] = camp_details['readcount'].str.split(' ').str[1]

        return camp_details
    # gocamp API 와 gocamp crawling merge
    def merge_data(self, camp, camp_details):
        merge_data = pd.merge(camp, camp_details, how='right', left_on='content_id', right_on='url_num')
        merge_data = merge_data.drop(['title', 'address'], 1)
        camp_df = merge_data.dropna(subset = ['addr'])
        camp_df = camp_df.reset_index().reset_index()
        camp_df = camp_df.drop(['index'],1)
        camp_df = camp_df.rename(columns={'level_0' : 'place_id',
                                    'img_url' : 'detail_image',
                                    'tags' : 'tag',
                                    'view' : 'readcount',
                                    })
        camp_df
        return camp_df

class Sigungucode:
    def __init__(self):
        self.do_list = {'충북': '충청북도', '충남': '충청남도',
               '경북': '경상북도', '경남': '경상남도',
               '전북': '전라북도', '전남': '전라남도',
               '강원': '강원도', '경기': '경기도',
               '인천': '인천광역시', '인천시': '인천광역시',
               '부산': '부산광역시', '울산': '울산광역시', '대전': '대전광역시',
               '대구': '대구광역시', '광주': '광주광역시',
               '서울': '서울특별시', '서울시': '서울특별시',
               '제주': '제주특별자치도', '제주도': '제주특별자치도'}


    def do_sigungu(self, df):
        df = df.drop(df[df['addr1'].isnull()].index, axis=0) # 빈 row 삭제
        # 예외처리 1: 페스티발 온라인개최 삭제
        try:
            df = df.drop(df[df['addr1'] == '온라인개최'].index, axis=0)
        except:
            pass

        # 도, 시군구명 컬럼 생성
        if not 'doNm' in df.columns.tolist():
            df['doNm'] = [a.split(" ")[0] for a in df['addr1']]
            df['doNm'] = [as_is.replace(as_is, self.do_list[as_is]) if len(as_is) < 3 else as_is for as_is in df['doNm']]
        if not 'sigunguNm' in df.columns.tolist():
            df['sigunguNm'] = [b.split(" ")[1:2] for b in df['addr1']]
            df['sigunguNm'] = [b[0] if len(b) > 0 else "" for b in df['sigunguNm']]

        df['sigunguNm2'] = [c.split(" ")[1:3] for c in df['addr1']]
        df['sigunguNm2'] = [c[0] + " " + c[1] if len(c) > 1 else "" for c in df['sigunguNm2']]
        df['sigunguNm3'] = [c.split(" ")[0:2] for c in df['addr1']]
        df['sigunguNm3'] = [c[0] + " " + c[1] if len(c) > 1 else "" for c in df['sigunguNm3']]

        # 예외처리 2: sigunguNm null값 처리
        sigunguNm = []
        for i in range(len(df)):
            a = df['sigunguNm'].iloc[i]
            b = df['sigunguNm2'].iloc[i]
            if type(a) == float:  # sigunguNm null값 예외처리
                result = b.split(" ")[0]
            else:
                result = a
            sigunguNm.append(result)
        df['sigunguNm'] = sigunguNm

        return df


    def make_sigungucode(self, df):
        df = self.do_sigungu(df)
        cursor.execute('SELECT * FROM sigungucode')
        query = cursor.fetchall()
        five_code = pd.DataFrame(data=query)
        # 조건에 맞게 시군구코드 생성
        signguNm_ls = five_code['signguNm'].unique().tolist()
        sigungucode = []

        for i in range(len(df)):
            a = df['sigunguNm'].iloc[i]
            b = df['sigunguNm2'].iloc[i]
            c = df['sigunguNm3'].iloc[i]
            d = df['doNm'].iloc[i]
            if a in signguNm_ls:
                result = five_code['signguCode'][five_code['signguNm'] == a].iloc[0]
            elif b in signguNm_ls:
                result = five_code['signguCode'][five_code['signguNm'] == b].iloc[0]
            elif c in signguNm_ls:
                result = five_code['signguCode'][five_code['signguNm'] == c].iloc[0]
            elif d in ['세종시', '세종특별자치시']:
                result = five_code['signguCode'][five_code['signguNm'] == '세종특별자치시'].iloc[0]
            else:
                result = '확인필요'
            sigungucode.append(result)

        # 시군구코드 컬럼 생성
        df['sigungucode'] = sigungucode

        # DB 저장시 필요없는 컬럼 삭제
        df.drop(['doNm', 'sigunguNm', 'sigunguNm2', 'sigunguNm3'], axis=1, inplace=True)

        return df


class PlaceSubTable():
    def place_table(self,camp_df):
        place_df = camp_df[['place_id', 'place_num', 'place_name', 'sigungu_code', 'addr', 'lat', 'lng',
                'first_image','tel', 'addr2', 'thema_envrn', 'tour_era',
                'homepage', 'line_intro', 'created_date', 'modified_date', 'detail_image', 'tag', 'readcount',
                'content_id', 'industry', 'oper_date', 'oper_pd',]]
        place_df = place_df.rename(columns={'place_id' : 'id'})
        return place_df

class Query:
    # db cursor 생성
    def connect_sql(self, IP, DB, PW):
        engine = create_engine(f"mysql+mysqldb://root:{PW}@{IP}/{DB}")

        conn = engine.connect()

        mydb = pymysql.connect(
            user='root',
            passwd=PW,
            host=IP,
            db=DB,
            charset='utf8',
        )
        cursor = mydb.cursor(pymysql.cursors.DictCursor)

        return cursor, engine, mydb

    # db에 저장
    def save_sql(self, cursor, engine, db, data, table, option):
        data.to_sql(name=table, con=engine, if_exists=option, index=False)


if __name__ == '__main__':
    IP = "34.136.89.21"
    DB = "camping"
    PW = "dss"

    gocamp = Gocamp()
    sgg = Sigungucode()
    sub = PlaceSubTable()
#     algo = AlgorithmTable()
    sql = Query()
    cursor, engine, db = sql.connect_sql(IP, DB, PW)

    # gocamp API
    df = gocamp.gocampingAPI()
    new_data = gocamp.update_date(df)
    camp_details = gocamp.make_camp_crawling(new_data)

    # sigungucode
    camp_api_df = sgg.make_sigungucode(new_data)
    camp = gocamp.make_camp_api(camp_api_df)

    # crawling and API files merge for the details
    camp_df = gocamp.merge_data(camp, camp_details)

    # camp info append insert to place table
    place_df = sub.place_table(camp_df)
    sql.save_sql(cursor, engine, db,  place_df, "place", "append")
    db.close()

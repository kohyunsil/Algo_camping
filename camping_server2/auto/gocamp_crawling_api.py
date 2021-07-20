from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import xmltodict
import json
from pandas.io.json import json_normalize
import pandas as pd
import re
import pymysql
from sqlalchemy import create_engine

pymysql.install_as_MySQLdb()
# import camping_server2.config as config

class Gocamp:
    base_url = "https://www.gocamping.or.kr"
    path = "/bsite/camp/info/list.do"
    query = "?pageUnit=3000&searchKrwd=&listOrdrTrget=last_updusr_pnttm"
    url = base_url + path + query

    df = pd.DataFrame()

    def __init__(self):
        self.secretKey = " "
   
    # gocamp crawling
    def fetch_link_list(self):
        print("👉 Start fetch camp list")
        response = requests.get(self.url)
        dom = BeautifulSoup(response.content, "html.parser")
        items = dom.select("#cont_inner > div > div.camp_search_list > ul > li")

        rows = []

        for item in items:
            new_row = {
                "title": item.select_one("h2 > a").text,
                # "description": item.select_one(".camp_stt").text,
                "address": item.select_one(".addr").text,
                # "contact": item.select_one("ul > li.call_num"),
                # "facility": item.select_one('i > span'),
                "view": item.select_one('div > div > p > span.item_t03').text,
                "link": "https://www.gocamping.or.kr" + item.select_one("div > a").get("href"),
                "tags": "",
                # "info": "",
                # "etc": "",
                "img_url": "",
                # "price": ""
            }
            rows.append(new_row)

        self.df = pd.DataFrame(rows)

    def fetch_link_details(self):
        self.df = self.df.fillna('')
        for idx in self.df.index:
            link = self.df.loc[idx, 'link']
            response = requests.get(link)
            dom = BeautifulSoup(response.text, "html.parser")
            # info = dom.select_one("table > tbody").text.strip()
            # info = info.replace("\t", " ").replace("\n", " ")
            # etc_info = dom.select_one("#table_type03 > div > table > tbody").text.strip()
            # etc_info = etc_info.replace("\t", " ").replace("\n", " ")
            imgs = dom.select('#contents > div > div.layout > div > div > div > a > img')
            #
            for img in imgs:
                self.df.loc[idx,"img_url"] = self.df.loc[idx,"img_url"] + str(img["src"]) + ","
            
            try:
                tags = dom.select_one("div.camp_tag > ul.tag_list").text.strip().replace("\n", " ")
            except:
                pass
            # pay_link = "https://www.gocamping.or.kr" + dom.select_one('#c_guide > a').get("href")

            self.df["tags"][idx] = tags
        #     # self.df["info"][idx] = info
        #     # self.df["etc"][idx] = etc_info
            # df["img_url"][idx] = img_url
        self.df["img_url"].str.split(",", expand=True)
        return self.df
    
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

    def make_camp_crawling(self) :
        camp_details = self.df.rename(columns={'view' : 'readcount'})
        camp_details['view'] = camp_details['view'].str.split(' ').str[1]
        datas = camp_details['link']
        data = [re.findall("\d+",data)[0] for data in datas]
        camp_details['url_num'] = data
        camp_details['url_num'] = camp_details['url_num'].astype('int')
        return camp_details

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
    def save_sql(self, cursor, engine, mydb, table):
        # sql append insert
        table.to_sql(name='place', con=engine, if_exists='append', index=False)


if __name__ == '__main__':
    IP = " "
    DB = " "
    PW = " "

    gocamp = Gocamp()
    cursor, engine, db = gocamp.connect_sql(IP, DB, PW)

    # gocamp crawling
    gocamp.fetch_link_list()
    gocamp.fetch_link_details()
    camp_details = gocamp.make_camp_crawling()
    
    # gocamp API
    camp_api_df = gocamp.gocampingAPI()
    camp = gocamp.make_camp_api(camp_api_df)
    
    # crawling and API merge for the details
    camp_df = gocamp.merge_data(camp, camp_details)
    
    # append insert
    gocamp.save_sql(cursor, engine, db, camp_df)

    db.close()
        



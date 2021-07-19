from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import time
import datetime
import json
from pandas.io.json import json_normalize
import xmltodict
import pandas as pd
import pymysql
from sqlalchemy import create_engine

pymysql.install_as_MySQLdb()
'''
한국관광공사 국문관광정보서비스 축제 & 관광지 API 자동화 코드
API_KEY, DB 정보는 생략 
'''
class FestivalTourApi:
    def __init__(self):
        self.secretKey = " "

    # 축제 API
    def festivalAPI(self, eventStartDate):
        """
        축제 검색 > 축제 시작일 설정
        eventStartDate: YYYYMMDD 양식으로 기입 (ex: 20210601)
        """
        url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchFestival?'
        param = 'ServiceKey=' + self.secretKey + '&MobileOS=ETC&MobileApp=AppTest&numOfRows=3000&arrange=A&listYN=Y'
        detail_param = f'&eventStartDate={eventStartDate}'

        request = Request(url + param + detail_param)
        request.get_method = lambda: 'GET'
        response = urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            responseData = response.read()
            rD = xmltodict.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)
            festival_api_df = json_normalize(rDD['response']['body']['items']['item'])

        return festival_api_df
    
    # 관광지 API
    def tourlistAPI(self, num):

        item_list = ["addr1", "addr2", "areacode", "booktour", "cat1", "cat2", "cat3", "contentid", "contenttypeid", "createdtime",
                     "firstimage", "firstimage2", "mapx", "mapy", "mlevel", "readcount", "sigungucode", "tel", "title", "zipcode"]
        data = pd.DataFrame()

        for z in item_list:
            globals()["{}_list".format(z)] = []

        # 정렬구분인 arange를 D(생성일순)으로 설정하여서 가장 최근 업데이트된 정보만 가져옴
        # pageno인 num인자 설정 필요 
        for i in range(num):
            url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey={}&contentTypeId=12&areaCode=&sigunguCode=&cat1=&cat2=&cat3=&listYN=Y&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&arrange=D&numOfRows=12&pageNo={}'.format(
                self.secretKey, i + 1)
            req = requests.get(url)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            item_order = len(soup.find_all('item'))

            for j in range(item_order):
                item_info = soup.find_all('item')[j]
                for z in item_list:
                    try:
                        globals()["{}".format(z)] = item_info.find_all(z)[0].text
                    except:
                        globals()["{}".format(z)] = None

                    globals()["{}_list".format(z)].append(globals()["{}".format(z)])
                    globals()["{}_df".format(z)] = pd.DataFrame(globals()["{}_list".format(z)]).rename(columns={0: z})
            time.sleep(1)

        for k in item_list:
            data = pd.concat([data, globals()["{}_df".format(k)]], 1)

        return data

    def update_date(self, data):
        # 자동화 실행 날기준으로 새롭게 업데이트된 정보만 가져옴
        diff_days = datetime.timedelta(days=14)
        today = datetime.date.today()
        last_day = today - diff_days
        last_day = last_day.isoformat().replace("-","")

        data['createdtime2'] = data['createdtime'].apply(lambda x: x[:8])
        new_data = data[data['createdtime2'] >= last_day]
        new_data = new_data.drop(["createdtime"],1)
        new_data = new_data.rename(columns={'createdtime2' : 'createdtime'})
        return new_data


    # 축제 정보   
    def make_festival(self, data):
        festival = data.drop(['areacode', 'cat1', 'cat2', 'cat3', 'contenttypeid', 'mlevel'], 1)
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
        return festival  

    # 관광지 정보
    def make_tour(self, data):
        tour = data.drop(['areacode', 'booktour', 'cat1', 'cat2', 'cat3', 'contenttypeid', 'mlevel', 
                    'zipcode'], 1)
        tour = tour.rename(columns={'addr1' : 'addr',
                            'contentid' : 'content_id',
                            'createdtime' : 'created_date',
                            'firstimage' : 'first_image',
                            'firstimage2' : 'second_image',
                            'mapx' : 'lat',
                            'mapy' : 'lng',
                            'sigungucode' : 'sigungu_code',
                            'title' : 'place_name'})
        tour['place_num'] = 2
        return tour
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

    ft_api = FestivalTourApi()
    cursor, engine, db = ft_api.connect_sql(IP, DB, PW)

    # 축제 API
    eventStartDate = datetime.date.today().isoformat().replace("-","")
    festival_api = ft_api.festivalAPI(eventStartDate)
    new_festival = ft_api.update_date(festival_api)
    update_festival = ft_api.make_festival(new_festival)

    # 관광지 API
    tour_api = ft_api.tourlistAPI(10)
    new_tour = ft_api.update_date(tour_api)
    update_tour = ft_api.make_tour(new_tour)

    # append insert
    ft_api.save_sql(cursor, engine, db, update_festival)
    ft_api.save_sql(cursor, engine, db, update_tour)

    db.close()
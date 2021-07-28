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
    # 정렬구분인 arange를 D(생성일순)으로 설정하여서 가장 최근 업데이트된 정보만 가져옴
    def festivalAPI(self):
        url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchFestival?'
        param = 'ServiceKey=' + self.secretKey + '&MobileOS=ETC&MobileApp=AppTest&numOfRows=3000&arrange=D&listYN=Y'

        request = Request(url + param)
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
    def save_sql(self, cursor, engine, mydb, table, option):
        # sql append insert
        table.to_sql(name='place', con=engine, if_exists=option, index=False)

class Sigungucode:
    def __init__(self):
        self.do_list = {'충북': '충청북도', '충남': '충청남도',
               '경북': '경상북도', '경남': '경상남도',
               '전북': '전라북도', '전남': '전라남도',
               '강원': '강원도', '경기': '경기도',
               '인천': '인천광역시', '인천시': '인천광역시',
               '부산': '부산광역시', '울산': '울산광역시', '대전': '대전광역시',
               '대구': '대구광역시', '광주': '광주광역시',
               '서울': '서울특별시', '서울시': '서울특별시', '세종': '세종특별자치시',
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

if __name__ == '__main__':
    IP = " "
    DB = " "
    PW = " "

    ft_api = FestivalTourApi()
    sgg = Sigungucode()
    cursor, engine, db = ft_api.connect_sql(IP, DB, PW)

    # 축제 API
    festival_api = ft_api.festivalAPI()
    festival = sgg.make_sigungucode(festival_api)
    new_festival = ft_api.update_date(festival)
    update_festival = ft_api.make_festival(new_festival)

    # 관광지 API
    tour_api = ft_api.tourlistAPI(10)
    tour = sgg.make_sigungucode(tour_api)
    new_tour = ft_api.update_date(tour)
    update_tour = ft_api.make_tour(new_tour)

    append insert
    ft_api.save_sql(cursor, engine, db, update_festival_df, "append")
    ft_api.save_sql(cursor, engine, db, update_tour_df, "append")

    db.close()

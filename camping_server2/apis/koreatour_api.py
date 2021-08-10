from urllib.request import Request, urlopen
import time
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import camping_server2.config as config
import xmltodict

class KoreaTourApi:
    def __init__(self):
        self.secretKey = config.Config.PUBLIC_API_KEY

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
            print(rDD)
            festival_api_df = json_normalize(rDD['response']['body']['items']['item'])

        return festival_api_df
        # festival_api_df.to_csv(config.Config.PATH + "festival_api_info.csv", encoding='utf-8-sig')



    def tourspotAPI(self, i, contentTypeId, radius=1000):
        """
        내 위치 기반 관광지 검색
        i: camp_api_df의 i번째 row 캠핑장 기준 검색
        contentType: 하단 contentType_dict 에서 골라 숫자 기입
         - contentType_dict= {'festival': 15, 'tourspot': 12, 'shopping': 38, 'restaurant': 39, }
        radius: 경도 위도 지점의 반경 몇 m 이내 검색 (default = 1000m)
        """
        camp_api_df = pd.read_csv(config.Config.PATH + "/camp_api_info.csv", encoding='utf-8-sig')

        mapX = camp_api_df['mapX'].iloc[i]
        mapY = camp_api_df['mapY'].iloc[i]

        url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList?'
        param = 'ServiceKey='+self.secretKey+'&MobileOS=ETC&MobileApp=AppTest&numOfRows=3000'
        detail_param = f'contentTypeId={contentTypeId}&mapX={mapX}&mapY={mapY}&radius={radius}&listYN=Y'

        request = Request(url+param+detail_param)
        request.get_method = lambda: 'GET'
        response = urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            responseData = response.read()
            # rDD_list = {}
            rD = xmltodict.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)
            # rDD_list.append(rDD)
            print(rDD)
            tourspot_api_df = json_normalize(rDD['response']['body']['items']['item'])
            return tourspot_api_df
            # tourspot_api_df.to_csv(config.Config.PATH + "tourspot_api_info.csv", encoding='utf-8-sig')

    # 지역 기반 관광지 검색
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

        # data.to_csv('tour_list.csv', index=False, encoding='utf-8-sig')

    def tour_estiDecoAPI(self, startYmd, endYmd):
        """
        관광지별 혼잡도 예측 집계 데이터 정보 조회
        startYmd/endYmd: YYYYMMDD 양식으로 기입 (ex: 20210601)
        startYmd = endYmd 의 경우, 1일 간의 결과값 조회
        """
        url = 'http://api.visitkorea.or.kr/openapi/service/rest/DataLabService/tarDecoList?'
        param = 'ServiceKey=' + self.secretKey + '&MobileOS=ETC&MobileApp=AppTest&numOfRows=10000'
        detail_param = f'&startYmd={startYmd}&endYmd={endYmd}'

        request = Request(url + param + detail_param)
        request.get_method = lambda: 'GET'
        response = urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            responseData = response.read()
            rD = xmltodict.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)
            print(rDD)
            tour_estiDeco_api_df = json_normalize(rDD['response']['body']['items']['item'])
            tour_estiDeco_api_df.to_csv(config.Config.PATH + "tour_estiDeco_api_info.csv", encoding='utf-8-sig')

    def visitors_API(self, region_type, startYmd, endYmd):
        """
        region_type: metco(광역시), locgo(지자체)
        일자 YYMMDD 형태로 기입
        기간 내 일별 데이터 조회
        """
        url = f'http://api.visitkorea.or.kr/openapi/service/rest/DataLabService/{region_type}RegnVisitrDDList?'
        param = 'ServiceKey=' + self.secretKey + '&MobileOS=ETC&MobileApp=AppTest&numOfRows=10000'
        detail_param = f'&startYmd={startYmd}&endYmd={endYmd}'

        request = Request(url + param + detail_param)
        request.get_method = lambda: 'GET'
        response = urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            responseData = response.read()
            rD = xmltodict.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)
            print(rDD)
            tour_estiDeco_api_df = json_normalize(rDD['response']['body']['items']['item'])
            tour_estiDeco_api_df.to_csv(config.Config.PATH + f"{region_type}_visitor_api_info.csv", encoding='utf-8-sig')
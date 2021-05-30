from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import xmltodict
import json
import pandas as pd
from pandas.io.json import json_normalize

class GocampingApi:
    def __init__(self):
        pass

    def get_secretKey(self):
        file = open("keys/api_secret_key.txt", "rt")
        secretKey = file.readline()
        file.close()
        return secretKey

    # 축제 검색 > 축제 시작일 설정
    def festivalAPI(self, eventStartDate):
        secretKey = self.get_secretKey()
        # eventStartDate = 20210601 #YYYYMMDD

        url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchFestival?'
        param = 'ServiceKey=' + secretKey + '&MobileOS=ETC&MobileApp=AppTest&numOfRows=3000&arrange=A&listYN=Y'
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
        festival_api_df.to_csv("../../datas/festival_api_info.csv", encoding='utf-8-sig')

    # 내 위치 기반 관광지 검색
    def tourspotAPI(self):
        secretKey = self.get_secretKey()
        contentType_dict = {'festival': 15, 'tourspot': 12, 'shopping': 38, 'restaurant': 39, }
        contentTypeId = contentType_dict['festival']
        camp_api_df = pd.read_csv("../../datas/camp_api_info.csv", encoding='utf-8-sig')

        i = 10
        mapX = camp_api_df['mapX'].iloc[i]
        mapY = camp_api_df['mapY'].iloc[i]

        url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList?'
        param = 'ServiceKey='+secretKey+'&MobileOS=ETC&MobileApp=AppTest&numOfRows=3000'
        detail_param = f'contentTypeId={contentTypeId}&mapX={mapX}&mapY={mapY}&radius=1000&listYN=Y'

        request = Request(url+param+detail_param)
        request.get_method = lambda: 'GET'
        response = urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            responseData = response.read()
            rDD_list = {}
            rD = xmltodict.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)
            # rDD_list.append(rDD)
            print(rDD)
            tourspot_api_df = json_normalize(rDD['response']['body']['items']['item'])
        tourspot_api_df.to_csv("../../datas/tourspot_api_info.csv", encoding='utf-8-sig')



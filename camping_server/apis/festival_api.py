from urllib.request import Request, urlopen
import xmltodict
import json
import pandas as pd
from pandas.io.json import json_normalize
import constant
import time

class KoreatourApi:
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
        festival_api_df.to_csv(constant.PATH + "festival_api_info.csv", encoding='utf-8-sig')

    # 내 위치 기반 관광지 검색
    def tourspotAPI(self):
        secretKey = self.get_secretKey()
        contentType_dict = {'festival': 15, 'tourspot': 12, 'shopping': 38, 'restaurant': 39, }
        contentTypeId = contentType_dict['festival']
        camp_api_df = pd.read_csv(constant.PATH + "camp_api_info.csv", encoding='utf-8-sig')

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
        tourspot_api_df.to_csv(constant.PATH + "tourspot_api_info.csv", encoding='utf-8-sig')


    # 지역 기반 관광지 검색
    def tourlistAPI(self, num):

        secretKey = self.get_secretKey()
        item_list = ["addr1", "addr2", "areacode", "booktour", "cat1", "cat2", "cat3", "contentid", "contenttypeid",
                     "firstimage", "firstimage2", "mapx", "mapy", "mlevel", "readcount", "sigungucode", "tel", "title", "zipcode"]
        data = pd.DataFrame()

        for z in item_list:
            globals()["{}_list".format(z)] = []

        for i in range(num):
            url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey={}&contentTypeId=12&areaCode=&sigunguCode=&cat1=&cat2=&cat3=&listYN=Y&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&arrange=A&numOfRows=12&pageNo={}'.format(
                secretKey, i + 1)
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

        data.to_csv('tour_list.csv', index=False, encoding='utf-8-sig')



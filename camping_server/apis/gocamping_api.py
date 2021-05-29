# !pip install urllib
# !pip install xmltodict
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import xmltodict
import json
import pandas as pd
from pandas.io.json import json_normalize

class gocampingApi:
    def __init__(self):
        pass

    def get_secretKey(self):
        file = open("keys/api_secret_key.txt", "rt")
        secretKey = file.readline()
        file.close()
        return secretKey

    def gocampingAPI(self):
        secretKey = self.get_secretKey()
        url = 'http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?'
        param = 'ServiceKey='+secretKey+'&MobileOS=ETC&MobileApp=AppTest&numOfRows=3000'

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
        camp_api_df.to_csv("../../datas/camp_api_info.csv", encoding='utf-8-sig')
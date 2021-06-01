import camping_server.constant as constant
from urllib.request import Request, urlopen
import xmltodict
import json
from pandas.io.json import json_normalize
import configparser

class GocampingApi:
    def __init__(self):
        config = configparser.RawConfigParser()
        config.read('keys/api_secret_key.ini')
        self.secretKey = config['API_KEYS']['PublicApiKey']

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
            camp_api_df.to_csv(constant.PATH + "test.csv", encoding='utf-8-sig')
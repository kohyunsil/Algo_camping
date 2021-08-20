from urllib.request import Request, urlopen
import time
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import xmltodict
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import algostar.config as config


class KoreaTourApi:
    def __init__(self):
        self.secretKey = config.Config.PUBLIC_API_KEY

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
            return tour_estiDeco_api_df

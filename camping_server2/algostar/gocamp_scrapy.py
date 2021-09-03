import requests
import re
import pandas as pd
from scrapy.http import TextResponse
from tqdm import tqdm
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import camping_server2.apis.gocamping_api as ga
gocamping = ga.GocampingApi()


class GocampCrawl:

    def view_crawler(self):
        '''
        월, 목 모두 크롤링
        '''
        url = "https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=3000&searchKrwd=&listOrdrTrget=last_updusr_pnttm"
        req = requests.get(url)
        response = TextResponse(req.url, body=req.text, encoding="utf-8")
        link = str(response.xpath('//*[@id="cont_inner"]/div/div/ul/li/div/a/@href').extract()).replace('read01', '')
        contentId = re.findall("\d+", link)
        view = str(response.xpath('//*[@id="cont_inner"]/div/div/ul/li/div/div/p/span[3]/text()').extract())
        view = re.findall("\d+", view)
        readcount = pd.concat([pd.DataFrame(contentId), pd.DataFrame(view)], 1)
        readcount.columns = ['contentId', 'readcount']

        return readcount

    def gocamp_crawler(self, time, date):
        ''' 신규캠핑장(월) 크롤링, date = createdtime,
           기존캠핑장(목) 크롤링, date = modifiedtime '''

        readcount = self.view_crawler()
        df = gocamping.gocampingAPI()
        df[f'{date}'] = df[f'{date}'].apply(lambda x: x.split(' ')[0])
        df[f'{date}'] = pd.to_datetime(df[f'{date}'])
        df = df.query(f'"{time}" <= {date}').reset_index(drop = True)
        contentIds = df.contentId

        base_url = "https://www.gocamping.or.kr"
        row = []
        for i in tqdm(contentIds):
            url = base_url + f"/bsite/camp/info/read.do?c_no={i}&viewType=read01&listOrdrTrget=last_updusr_pnttm"
            try:
                req = requests.get(url)
                response = TextResponse(req.url, body = req.text, encoding = "utf-8")
                new_row = {"contentId" : i,
                           "tags" : response.xpath('//*[@id="sub_title_wrap2"]/div[2]/div[2]/ul/li/text()').extract()}

            except requests.exceptions.ChunkedEncodingError:
                # data = df[df['contentId'] == i].facltNm.unique()
                new_row = {"contentId": i,
                       "tags": "" }

            row.append(new_row)

        new_tag = pd.DataFrame(row)
        new_camp = pd.merge(new_tag, readcount, how='left')
        new_camp['tags'] = new_camp['tags'].apply(', '.join)
        # new_camp.to_csv('../../datas/crawling_data.csv', encoding='utf-8-sig', index=False)
        return new_camp
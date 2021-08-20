import camping_server2.config as config
from fake_useragent import UserAgent
import json
import pandas as pd
import requests

class Scraping:
    def __init__(self, search_target):
        ua = UserAgent()
        self.search_target = search_target
        self.user_agent = ua.random

    # xhr request url에 들어가는 id 파라미터 값 얻기
    def get_params(self):
        ids, place_name = [], []

        for target in self.search_target[:]:
            query_url = f'https://m.map.naver.com/search2/searchMore.naver?query={target}&sm=clk&style=v5&page=1&displayCount=75&type=SITE_1'
            headers = {'User-Agent': self.user_agent}
            response = requests.get(query_url, headers=headers)

            try:
                json_res = json.loads(response.text)
                print(json_res)
                target_id = json_res['result']['site']['list'][0]['id'].split('s')[1]
                ids.append(target_id)
                place_name.append(target)
            except:
                ids.append('')
                place_name.append(target)
                continue

        return ids, place_name

    def to_csv(self, res_reviews, place_name):
        v4_blog = pd.DataFrame()

        for i, res in enumerate(res_reviews):
            if res == '':
                continue
            else:
                try:
                    res = json.loads(res)
                    items = res['result']['itemList']
                except:
                    continue

                for item in items:
                    item['place_name'] = place_name[i]
                    v4_blog = v4_blog.append(item, ignore_index=True)
                v4_blog.to_csv(config.Config.PATH + 'v4_test.csv', encoding='utf-8-sig', header=True)

    def get_reviews(self, ids, place_name):
        res_reviews = []

        for i, id in enumerate(ids):
            xhr_url = f'https://v4.map.naver.com/local/searchPost.nhn?display={constant.MAX_PAGE}&page=1&code={id}'
            headers = {'User-Agent': self.user_agent}
            response = requests.get(xhr_url, headers=headers)
            res_reviews.append(response.text)

        self.to_csv(res_reviews, place_name)
        return res_reviews

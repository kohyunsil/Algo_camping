from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import pandas as pd
import camping_server2.config as config

class CampCrawler:
    base_url = "https://www.gocamping.or.kr"
    path = "/bsite/camp/info/list.do"
    query = "?pageUnit=3000&searchKrwd=&listOrdrTrget=last_updusr_pnttm"
    url = base_url + path + query

    df = pd.DataFrame()

    def fetch_camp_list(self):
        print("👉 Start fetch camp list")
        response = requests.get(self.url)
        dom = BeautifulSoup(response.content, "html.parser")
        items = dom.select("#cont_inner > div > div.camp_search_list > ul > li")

        rows = []

        for item in items:
            new_row = {
                "title": item.select_one("h2 > a").text,
                "description": item.select_one(".camp_stt").text,
                "address": item.select_one(".addr").text,
                "contact": item.select_one("ul > li.call_num"),
                "facility": item.select_one('i > span'),
                "view": item.select_one('div > div > p > span.item_t03').text,
                "link": "https://www.gocamping.or.kr" + item.select_one("div > a").get("href"),
                "tags": "",
                "info": "",
                "etc": "",
                "img_url": "",
                "price": ""
            }
            rows.append(new_row)

        self.df = pd.DataFrame(rows)
        # print("👉 Finish fetch camp list")

    def fetch_camp_details(self):
        for idx in tqdm(self.df.index):
            link = self.df.loc[idx, 'link']
            response = requests.get(link)
            dom = BeautifulSoup(response.text, "html.parser")
            tags = dom.select_one("div.camp_tag > ul.tag_list ").text.strip().replace("\n", " ")
            info = dom.select_one("table > tbody").text.strip()
            info = info.replace("\t", " ").replace("\n", " ")
            etc_info = dom.select_one("#table_type03 > div > table > tbody").text.strip()
            etc_info = etc_info.replace("\t", " ").replace("\n", " ")
            imgs = dom.select('#contents > div > div.layout > div > div > div > a > img')
            img_url = []

            for img in imgs:
                img_url.append(img['src'])
            pay_link = "https://www.gocamping.or.kr" + dom.select_one('#c_guide > a').get("href")

            self.df["tags"][idx] = tags
            self.df["info"][idx] = info
            self.df["etc"][idx] = etc_info
            self.df["img_url"][idx] = img_url

            try:
                self.df["price"][idx] = self.__fetch_camp_price(pay_link)
            except AttributeError as e:
                self.df["price"][idx] = ""

        self.df.to_csv(config.Config.PATH + "details.csv", index=False, encoding="utf-8-sig")

    def __fetch_camp_price(self, link):
        response = requests.get(link)
        dom = BeautifulSoup(response.text, "html.parser")
        price = dom.select_one(
            '#contents > div > div.layout > div.camp_intro > div > table > tbody > tr').text.strip().replace("\n", " ")

        return price
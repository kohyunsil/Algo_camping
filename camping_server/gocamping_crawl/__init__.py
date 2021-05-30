import gocamp_crawl as gc
import pandas as pd

if __name__ == '__main__':
    crawler = gc.CampCrawler()
    crawler.fetch_camp_list()
    crawler.fetch_camp_details()
    result = crawler.df
    result.to_csv("../../datas/details.csv", index=False, encoding="utf-8-sig")
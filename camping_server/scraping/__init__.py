import kakao_reviews as kr
import naverv4_blog as nv4
import gocamp_crawl as gc
import camping_server.config as config
import pandas as pd

def target_list():
    datas = pd.read_csv(config.Config.PATH + 'tour_list.csv')
    datas = datas[['title']]
    name = datas.iloc[:]['title']
    search_target = [target.lstrip() for target in name.tolist()]

    return search_target

if __name__ == '__main__':
    # s = kr.Scraping()
    # s.get_search(target_list())

    # v4 = nv4.Scraping(target_list())
    # ids, place_name = v4.get_params()
    # res_reviews = v4.get_reviews(ids, place_name)

    # crawler = gc.CampCrawler()
    # crawler.fetch_camp_list()
    # crawler.fetch_camp_details()
    # result = crawler.df

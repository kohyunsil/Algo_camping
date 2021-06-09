import kakao_reviews as kr
import naverv4_blog as nv4
import gocamp_crawl as gc
import camping_server.config as config
import time
import naverv5_category as nv5
import camping_server.scraping.ogcamp_crawl as oc
import pandas as pd

def target_list():
    """
    get gocamping title list
    :return:
    gocamping title
    """
    datas = pd.read_csv(config.Config.PATH + '/camp_detail_page.csv')
    datas = datas[['title']]
    name = datas.iloc[:]['title']
    search_target = [target.split(']')[1].strip() for target in name.tolist()]

    return search_target

def get_nv5_result(camping_list):
    """
    naverv5 category review scraping
    :param camping_list:
    :return:
    naver map v5 category review crawling result csv
    """
    highlight_reviews = []
    try:
        for title in camping_list:
            s = nv5.CategoryScraping(title)
            s.switch_iframe()

            title = s.move_tab()
            print(title)
            if title == '':
                continue
            category = s.get_categories()
            cnt = 1
            try:
                while True:
                    try:
                        target_category = s.click_cagetory(category, cnt)
                    except:
                        break
                    else:
                        elements = s.scroll_down(config.Config.COUNT)
                        for j, element in enumerate(elements[:config.Config.COUNT]): # default 100
                            try:
                                info = s.get_reviews(title, target_category, j)
                                highlight_reviews.append(info)
                            except:
                                break
                        cnt += 1
            finally:
                s.driver.quit()
                time.sleep(2)
    finally:
        print(highlight_reviews)
        s.save_res(highlight_reviews)

if __name__ == '__main__':
    camping_list = target_list()
    get_nv5_result(camping_list[:])

    # s = kr.Scraping()
    # s.get_search(target_list())

    # v4 = nv4.Scraping(target_list())
    # ids, place_name = v4.get_params()
    # res_reviews = v4.get_reviews(ids, place_name)

    # crawler = gc.CampCrawler()
    # crawler.fetch_camp_list()
    # crawler.fetch_camp_details()
    # result = crawler.df
    
    # ogcamp = oc.OgcampScraping()
    # ogcamp.get_data()
    
    # ogcamp = oc.OgcampScraping()
    # ogcamp.get_data()
    # ogcamp.get_details()
    

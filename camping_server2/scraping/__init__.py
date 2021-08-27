import datetime
import config as config
import time
import naverv5_category as nv5
import pandas as pd


def target_list():
    """
    get gocamping title list
    :return:
    gocamping title
    """
    datas = pd.read_csv(config.Config.PATH + '/info.csv')
    name = datas['name']
    # name = name.iloc[:]['title']

    base_addr = datas['addr']
    # base_addr = base_addr.iloc[:]['addr']

    return list(name), list(base_addr)


def get_nv5_result(camping_list, camping_addrs):
    """
    naverv5 category review scraping
    :param camping_list, camping_addrs:
    :return:
    naver map v5 category review crawling result csv
    """
    highlight_reviews = []
    try:
        for i, camping_title in enumerate(camping_list):
            s = nv5.CategoryScraping(camping_title)
            s.switch_iframe()

            title, addr = s.move_tab()
            print(title, addr)
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
                        for j, element in enumerate(elements[:config.Config.COUNT]):  # default 100
                            try:
                                info = s.get_reviews(camping_title, camping_addrs[i], addr, target_category, j)
                                highlight_reviews.append(info)
                            except:
                                break
                        cnt += 1
            finally:
                s.driver.quit()
                time.sleep(2)
                # slackbot.IncomingWebhook.send_msg(f'{datetime.datetime.now()}  {i}번째 {camping_title}까지 완료')

    finally:
        print(highlight_reviews)
        s.save_res(highlight_reviews)
        # slackbot.IncomingWebhook.send_msg(f'crawling completed ! result line num : {len(highlight_reviews)}')

if __name__ == '__main__':
    camping_list, camping_addrs = target_list()
    get_nv5_result(camping_list[10:20], camping_addrs[10:20])
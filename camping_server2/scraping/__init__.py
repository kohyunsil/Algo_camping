import kakao_reviews as kr
import datetime
from bot import slackbot
import config as config
import time
import pandas as pd

def target_list():
    """
    get gocamping title list
    :return:
    gocamping title
    """
    datas = pd.read_csv(config.Config.PATH + '/target_list.csv')
    name = datas[['title']]
    name = name.iloc[:]['title']

    base_addr = datas[['addr']]
    base_addr = base_addr.iloc[:]['addr']

    return list(name), list(base_addr)


if __name__ == '__main__':
    camping_list, camping_addrs = target_list()

    s = kr.Scraping()
    s.get_search(target_list())

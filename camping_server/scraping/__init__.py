import kakao_reviews as kr
import naverv4_blog as nv4
import constant
import pandas as pd

def target_list():
    datas = pd.read_csv(constant.PATH + 'info.csv')
    datas = datas[['name', 'addr']]
    name = datas.iloc[:]['name']
    search_target = [target.lstrip() for target in name.tolist()]

    return search_target

if __name__ == '__main__':
    # s = kr.Scraping()
    # s.get_search(target_list())  # 캠핑장 업소명 리스트

    v4 = nv4.Scraping(target_list())
    ids = v4.get_params()
    print(f'ids: {ids}')
    res_reviews = v4.get_reviews(ids)
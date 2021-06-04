import pyautogui
import camping_server.config as constant
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import json
import time
import requests
import pandas as pd
import requests

ids = []

def target_list():
    datas = pd.read_csv(constant.PATH + 'info.csv')
    datas = datas[['name', 'addr']]
    name = datas.iloc[:]['name']
    search_target = [target.lstrip() for target in name.tolist()]

    return search_target

# xhr request url에 들어가는 id 파라미터 값 얻기
def get_params(user_agent, target):
    query_url = f'https://m.map.naver.com/search2/searchMore.naver?query={target}&sm=clk&style=v5&page=1&displayCount=75&type=SITE_1'
    headers = {'User-Agent': user_agent}
    response = requests.get(query_url, headers=headers)

    try:
        json_res = json.loads(response.text)
        target_id = json_res['result']['site']['list'][0]['id'].split('s')[1]
        ids.append(target_id)
    except:
        ids.append('')


if __name__ == '__main__':
    search_target = target_list()
    ua = UserAgent()
    user_agent = ua.random

    for target in search_target[:]:
        get_params(user_agent, target)

    for i, id in enumerate(ids):
        xhr_url = f'https://map.naver.com/v5/search/{search_target[i]}/place/{int(id)}'
        print(xhr_url)

        # 첫번째 화면 request payload
        # query = '{"logLevel":"info","module":"Performance","className":"CommonRoutesService","methodName":"detectLastNavigationEnd","msg":"Browser Load Time","body":"{\"componentName\":\"t\"}","browserName":"Chrome","browserVersion":"90.0.4430.212","projectName":"blackpearl","projectVersion":"2.0.0","env":"real","userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"'
        # query += f',"url":"https://map.naver.com/v5/search/{search_target[i]}/place/{int(id)}?c=14118781.0941358,4507460.2618540,15,0,0,0,dh","logger":null' + "}"

        # payload 두번째 시도
        # query = '{"operationName":"getVisitorReviews","variables":{"input":{'
        # query += f'"businessId":"{int(id)}","businessType":"accommodation","item":"0","bookingBusinessId":null,"page":1,"display":10,"isPhotoUsed":false,"theme":"allTypes","includeContent":true,"getAuthorInfo":true'
        # query += '}},"query":"query getVisitorReviews($input: VisitorReviewsInput){\n  visitorReviews(input: $input) {\n    items {\n      id\n      rating\n      author {\n        id\n        nickname\n        from\n        imageUrl\n        objectId\n        url\n        review {\n          totalCount\n          imageCount\n          avgRating\n          __typename\n        }\n        __typename\n      }\n      body\n      thumbnail\n      media {\n        type\n        thumbnail\n        __typename\n      }\n      tags\n      status\n      visitCount\n      viewCount\n      visited\n      created\n      reply {\n        editUrl\n        body\n        editedBy\n        created\n        replyTitle\n        __typename\n      }\n      originType\n      item {\n        name\n        code\n        options\n        __typename\n      }\n      language\n      highlightOffsets\n      translatedText\n      businessName\n      showBookingItemName\n      showBookingItemOptions\n      bookingItemName\n      bookingItemOptions\n      __typename\n    }\n    starDistribution {\n      score\n      count\n      __typename\n    }\n    hideProductSelectBox\n    total\n    __typename\n  }\n}\n"},{"operationName":"getVisitorReviews", "variables":{'
        # query += f'"id":"{int(id)}"'
        # query += '},"query":"query getVisitorReviews($id: String) {\n  visitorReviewStats(input: {businessId: $id}) {\n    id\n    name\n    review {\n      avgRating\n      totalCount\n      scores {\n        count\n        score\n        __typename\n      }\n      starDistribution {\n        count\n        score\n        __typename\n      }\n      imageReviewCount\n      authorCount\n      maxSingleReviewScoreCount\n      maxScoreWithMaxCount\n      __typename\n    }\n    visitorReviewsTotal\n    ratingReviewsTotal\n    __typename\n  }\n  visitorReviewThemes(input: {businessId: $id}) {\n    themeLists {\n      name\n      key\n      __typename\n    }\n    __typename\n  }\n}\n"}, {"operationName":"getVisitorReviewPhotosInVisitorReviewTab","variables":{'
        # query +=  f'"businessId":"{int(id)}","businessType":"accommodation","item":"0","theme":"allTypes","page":1,"display":10'
        # query += '},query":"query getVisitorReviewPhotosInVisitorReviewTab($businessId: String!, $businessType: String, $page: Int, $display: Int, $theme: String, $item: String)'
        # query += '{\n  visitorReviews(input: {businessId: $businessId, businessType: $businessType, page: $page, display: $display, theme: $theme, item: $item, isPhotoUsed: true}) {\n    items {\n      id\n      rating\n      author {\n        id\n        nickname\n        from\n        imageUrl\n        objectId\n        url\n        __typename\n      }\n      body\n      thumbnail\n      media {\n        type\n        thumbnail\n        __typename\n      }\n      tags\n      status\n      visited\n      originType\n      item {\n        name\n        code\n        options\n        __typename\n      }\n      businessName\n      __typename\n    }\n    starDistribution {\n      score\n      count\n      __typename\n    }\n    hideProductSelectBox\n    total\n    __typename\n  }\n}\n"},'
        # query += '{"operationName":"getVisitorRatingReviews","variables":{"input":{"'
        # query += f'"id":"{int(id)}"'
        # query += '},"query":"query getVisitorRatingReviews($input: VisitorReviewsInput) {\n  visitorReviews(input: $input) {\n    total\n    items {\n      id\n      rating\n      author {\n        id\n        nickname\n        from\n        imageUrl\n        objectId\n        url\n        review {\n          totalCount\n          imageCount\n          avgRating\n          __typename\n        }\n        __typename\n      }\n      visitCount\n      visited\n      originType\n      reply {\n        editUrl\n        body\n        editedBy\n        created\n        replyTitle\n        __typename\n      }\n      businessName\n      status\n      __typename\n    }\n    __typename\n  }\n}\n"}'

        # payload 세번째 시도
        query = '{"operationName": "getVisitorRatingReviews", "variables": {"input": {'
        query += f'"businessId": "{int(id)}",'
        query += '"businessType": "accommodation", "item": "0", "bookingBusinessId": null, "page": 1, "display": 10, "includeContent": false, "getAuthorInfo": true},'
        query += f'"id": "{int(id)}"'
        query += '},"query": "query getVisitorRatingReviews($input: VisitorReviewsInput) {\n  visitorReviews(input: $input) {\n    total\n    items {\n      id\n      rating\n      author {\n        id\n        nickname\n        from\n        imageUrl\n        objectId\n        url\n        review {\n          totalCount\n          imageCount\n          avgRating\n          __typename\n        }\n        __typename\n      }\n      visitCount\n      visited\n      originType\n      reply {\n        editUrl\n        body\n        editedBy\n        created\n        replyTitle\n        __typename\n      }\n      businessName\n      status\n      __typename\n    }\n    __typename\n  }\n}\n"}'

        print(query)
        headers = {
            'User-Agent': user_agent,
            'Content-Type': 'text/plain; charset=utf-8',
            'Referer': 'https://map.naver.com/'
        }

        # graphql request url
        req_url = 'https://pcmap-api.place.naver.com/graphql'
        response = requests.post(req_url, json=query.encode('utf-8'), headers=headers)
        print(response)
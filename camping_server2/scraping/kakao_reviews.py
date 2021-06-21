import camping_server2.config as config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import time
import requests
import pandas as pd

result = []

class Scraping:
    def __init__(self):
        self.user_agent = UserAgent().random
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.set_window_size(200, 200)
        self.url = 'https://map.kakao.com/'
        self.driver.get(self.url)

    # 초기 배너 제거
    def remove_banner(self):
        try:
            position = self.driver.find_element_by_xpath('/html/body/div[10]/div/div/img')
            action = webdriver.common.action_chains.ActionChains(self.driver)
            action.move_to_element_with_offset(position, 100, 100)
            action.click()
            action.perform()
        except:
            pass

    def get_reviews(self, place):
        driver = self.driver
        time.sleep(2)
        page = 0

        # XHR response
        while True:
            try:
                # current request URL
                req_url = driver.current_url
                req_path = int(req_url.split('/')[3].split('#')[0])

                # request url
                xhr_url = f'https://place.map.kakao.com/commentlist/v/{req_path}/{page}?platform='

                # Referer, User-Agent
                headers = {
                    'Referer': f'https://place.map.kakao.com/{req_path}',
                    'User-Agent': self.user_agent
                }

                response = requests.get(xhr_url, headers=headers)
                print('XHR response num : ', len(response.json()['comment']['list']))  # response len 체크
                res_data = response.json()['comment']['list']

                for r in res_data:
                    r['place_name'] = place

                result.append(res_data)
                page += 1

            except:
                break

        driver.close()
        driver.switch_to_window(driver.window_handles[0])

    def move_page(self, place):
        driver = self.driver
        # 초기 배너 제거
        self.remove_banner()

        try:
            href = driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li[1]/div[4]/span[1]/a')
            href.send_keys(Keys.CONTROL + '\n')
            driver.switch_to.window(driver.window_handles[1])
            self.get_reviews(place)

        except:
            return

    def to_csv(self):
        kakao_reviews = pd.DataFrame()

        for r in result:
            if r == '':
                continue
            else:
                for i in r:
                    kakao_reviews = kakao_reviews.append(i, ignore_index=True)

        kakao_reviews = kakao_reviews.drop('commentid', axis=1)
        kakao_reviews.to_csv(config.Config.PATH + 'tour_3000.csv', encoding='utf-8-sig', header=True)

    def get_search(self, search_target):
        driver = self.driver

        for target in search_target[:]:
            time.sleep(2)
            input_element = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')
            input_element.clear()
            input_element.send_keys(target, Keys.RETURN)
            time.sleep(2)
            self.move_page(target)

        driver.quit()
        self.to_csv()
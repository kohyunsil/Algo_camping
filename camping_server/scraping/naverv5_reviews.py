from selenium.common.exceptions import NoSuchElementException

import camping_server.config as config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

class Scraping:
    def __init__(self):
        self.user_agent = UserAgent().random
        self.url = 'https://map.naver.com/v5/'
        driver.get(self.url)
        time.sleep(2)

    def get_list(self):
        keyword = "캠핑장"
        driver.find_element_by_xpath('//*[@id="container"]/shrinkable-layout/div/app-base/search-input-box/div/div/div/input').send_keys(keyword)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="container"]/shrinkable-layout/div/app-base/search-input-box/div/div[2]/div/div/instant-search-list/div/div/nm-list-container[1]/div/nm-list/ul/li[1]/a').click()
        time.sleep(2)

        iframe = driver.find_element_by_xpath('//*[@id="searchIframe"]')
        driver.switch_to.frame(iframe)
        items = driver.find_elements_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul/li')
        len(items)
        return items

    def move_detail(self, items):
        for i in range(len(items))[:5]:
            items[i].find_element_by_xpath('div[1]/a').click()
            driver.switch_to.default_content()
            time.sleep(2)
            iframe = driver.find_element_by_css_selector('#entryIframe')
            time.sleep(2)
            driver.switch_to.frame(iframe)
            time.sleep(2)

            menus = driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[3]/div/div/div/div').text
            menus = str(menus).split(' ')
            # print(menus)
            try:
                review_idx = menus.index('리뷰')
                driver.find_element_by_xpath(f'//*[@id="app-root"]/div/div[2]/div[3]/div/div/div/div/a[{review_idx + 1}]').click()
            except:
                # iframe close
                print('index error!!')
                pass

            time.sleep(2)
            count = 10
            try:
                while count:
                    driver.execute_script('window.scrollTo(0, 10000);')
                    driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[2]/a').click()
                    time.sleep(1)
                    count -= 1
            except:
                print("end")
                driver.find_element_by_xpath('//*[@id="container"]/shrinkable-layout/div/app-base/search-layout/div[2]/entry-layout/entry-close-button/button').click()
                continue

            time.sleep(2)
            try:
                elements = driver.find_elements_by_xpath('//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/ul/li')
                print(f'len:{len(elements)}')
            except:
                print('no element')

            datas = []
            for element in elements[:3]:
                data = {}
                try:
                    if element.find_element_by_xpath('div/div[1]/a/div/div[1]').text != '':
                        data["username"] = element.find_element_by_xpath('div/div[1]/a/div/div[1]').text
                    else:
                        raise e('username')
                    if element.find_element_by_xpath('div/div[1]/a/div/div[2]/span[1]').text.split(" ")[1] != '':
                        data["review_count"] = element.find_element_by_xpath('div/div[1]/a/div/div[2]/span[1]').text.split(" ")[1]
                    else:
                        raise e('review_count')
                    if element.find_element_by_xpath('div/div[2]/div[1]/span[2]').text != '':
                        data["star"] = element.find_element_by_xpath('div/div[2]/div[1]/span[2]').text
                    else:
                        raise e('star')
                except NoSuchElementException as e:
                    print('error:', e)
                    data[e] = ''
                else:
                    datas.append(data)
                    print(datas)
                driver.quit()


if __name__ == '__main__':
    s = Scraping()
    items = s.get_list()
    s.move_detail(items)

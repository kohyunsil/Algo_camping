from selenium.webdriver.common.keys import Keys
import camping_server.config as config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import re
import time

"""
네이버 지도 v5 메인에 노출된 '캠핑장' 카테고리 리스트 리뷰 크롤링
"""
class Scraping:
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.user_agent = UserAgent().random
        self.url = 'https://map.naver.com/v5/'
        self.driver.get(self.url)
        time.sleep(2)

    def switch_iframe(self):
        iframe = self.driver.find_element_by_xpath('//*[@id="searchIframe"]')
        self.driver.switch_to.frame(iframe)
        items = self.driver.find_elements_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul/li')

        items[0].find_element_by_xpath('div[1]/a').click()
        self.driver.switch_to.default_content()
        time.sleep(2)
        iframe = self.driver.find_element_by_css_selector('#entryIframe')
        time.sleep(2)
        self.driver.switch_to.frame(iframe)
        time.sleep(2)

        return items

    def get_list(self):
        keyword = "캠핑장"
        try:
            self.driver.find_element_by_xpath('//*[@id="container"]/shrinkable-layout/div/app-base/search-input-box/div/div/div/input').send_keys(keyword)
            time.sleep(2)
            self.driver.execute_script('window.scrollTo(0, 10000);')
            self.driver.find_element_by_xpath('//*[@id="container"]/shrinkable-layout/div/app-base/search-input-box/div/div[2]/div/div/instant-search-list/div/div/nm-list-container[1]/div/nm-list/ul/li[1]/a').click()
            time.sleep(2)

            items = self.switch_iframe()
        except:
            pass
        finally:
            return items

    def move_detail(self, items):
        menus = self.driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[3]/div/div/div/div').text
        menus = str(menus).split(' ')
        try:
            review_idx = menus.index('리뷰')
            self.driver.find_element_by_xpath(
                f'//*[@id="app-root"]/div/div[2]/div[3]/div/div/div/div/a[{review_idx + 1}]').click()
        except:
            print('Index Error')
            self.driver.switch_to.default_content()

        time.sleep(2)
        count = 2
        try:
            while count:
                self.driver.execute_script('window.scrollTo(0, 10000);')
                self.driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[2]/a').click()
                time.sleep(1)
                count -= 1
        except:
            print("Scroll End")

        time.sleep(2)
        elements = self.driver.find_elements_by_xpath('//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/ul/li')
        len(elements)

        time.sleep(2)
        try:
            elements = self.driver.find_elements_by_xpath('//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/ul/li')
            print(f'element length:{len(elements)}')
        except:
            print('No Element')

        datas = []
        for i, element in enumerate(elements[:4]):
            data = {}
            try:
                target = element.find_element_by_xpath('div').text
                num = 1
                if target.split('\n')[num - 1] != '프로필':
                    continue

                data['user_name'] = target.split('\n')[num]

                review_pattern = re.compile(r'(\d)')
                data['review_count'] = review_pattern.findall(target.split('\n')[num + 1].split('리뷰 ')[num])[0]

                data['mean_star'] = target.split('\n')[num + 3]

                while True:
                    if target.split('\n')[num + 4] != '리뷰이미지':
                        break
                    else:
                        num += 1

                data['star'] = target.split('\n')[num + 4]

                date_pattern = re.compile(r'(\d{4}.\d{2}.\d{2})')
                data['date'] = date_pattern.findall(target.split('\n')[num + 5])[0]

                visit_pattern = re.compile(r'\d' + '번째')
                data['visit_count'] = visit_pattern.findall(target.split('\n')[num + 5])[0].split('번째')[0]

                data['review'] = target.split('\n')[num + 7]

            except:
                print('NoSuchElement Error')
                datas.append(data)
                continue
            else:
                datas.append(data)

        print(datas)
        # switch iframe
        self.driver.switch_to.default_content()
        iframe = self.driver.find_element_by_xpath('//*[@id="searchIframe"]')
        self.driver.switch_to.frame(iframe)

        # search list
        items[1].find_element_by_xpath('div[1]/a').click()
        time.sleep(2)
        iframe = self.driver.find_element_by_css_selector('#entryIframe')
        time.sleep(2)
        self.driver.switch_to.frame(iframe)
        time.sleep(2)
        self.driver.quit()


if __name__ == '__main__':
    s = Scraping()
    items = s.get_list()
    s.move_detail(items)

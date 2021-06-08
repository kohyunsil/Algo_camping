from selenium import webdriver
import time
import pandas as pd
import re


class CategoryScraping:
    """
    네이버 지도 v5 '캠핑장' 카테고리별 하이라이트 리뷰 크롤링
    """
    def __init__(self, keyword):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.url = f"https://map.naver.com/v5/search/{keyword}"
        self.driver.get(self.url)

    def switch_iframe(self):
        """main search list iframe switch (1)"""
        iframe = self.driver.find_element_by_xpath('//*[@id="searchIframe"]')
        self.driver.switch_to.frame(iframe)

        time.sleep(2)
        items = self.driver.find_elements_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul/li')
        print(len(items))
        items[0].find_element_by_xpath('div[1]/a').click()
        self.driver.switch_to.default_content()
        time.sleep(1)
        iframe = self.driver.find_element_by_css_selector('#entryIframe')
        time.sleep(1)
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

    def move_tab(self):
        """enter iframe + click review tab (2)"""
        title = self.driver.find_element_by_xpath('//*[@id="_title"]/span[1]').text
        menus = self.driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[3]/div/div/div/div').text
        menus = str(menus).split(' ')

        try:
            review_idx = menus.index('리뷰')
            self.driver.find_element_by_xpath(
                f'//*[@id="app-root"]/div/div[2]/div[3]/div/div/div/div/a[{review_idx + 1}]').click()
        except:
            print('Index Error')
            self.driver.switch_to.default_content()
        time.sleep(1)

        return title

    def click_category(self, idx=0):
        """ select category (3)"""
        print(self.driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/div[1]/div').text)
        category = self.driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/div[1]/div')

        # click category
        time.sleep(1)
        target_category = category.find_element_by_xpath(f'//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/div[1]/div/a[{idx + 1}]')
        print(target_category.text)
        time.sleep(2)
        webdriver.ActionChains(self.driver).move_to_element(target_category).click(target_category).perform()

        return target_category

    def scroll_down(self, count=5):
        """selected category scroll down (4)"""
        # scroll down
        while count:
            self.driver.execute_script('window.scrollTo(0, 10000);')
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[2]/a').click()
            count -= 1

        # all li element
        time.sleep(1)
        try:
            elements = self.driver.find_elements_by_xpath('//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/ul/li')
        except:
            print('No Element')
        else:
            return elements

    def get_reviews(self, title, target_category):
        """selected category review scraping (5)"""
        # get highlight reviews
        try:
            span = self.driver.find_element_by_xpath(
                f'//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/ul/li[{j + 1}]/div[1]/div[5]/a')
        except:
            try:
                span = self.driver.find_element_by_xpath(
                    f'//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/ul/li[{j + 1}]/div[1]/div[4]/a')
            except:
                try:
                    span = self.driver.find_element_by_xpath(
                        f'//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/ul/li[{j + 1}]/div/div[4]/a')
                except:
                    try:
                        span = self.driver.find_element_by_xpath(
                            f'//*[@id="app-root"]/div/div[2]/div[5]/div[4]/div[4]/div[1]/ul/li[{j + 1}]/div/div[5]/a')
                    except:
                        print('No Highlight review div')

        # 하나의 div element에 대한 사용자 리뷰 정보 가져오기
        try:
            info = {}
            highlight = span.find_element_by_class_name('highlight').text

            info['category'] = target_category.text
            info['title'] = title
            info['highlight_review'] = highlight

            target = element.find_element_by_xpath('div').text
            cnt = 1
            if target.split('\n')[cnt - 1] != '프로필':
                pass
            info['user_name'] = target.split('\n')[cnt]

            review_pattern = re.compile(r'(\d)')
            info['review_count'] = review_pattern.findall(target.split('\n')[cnt + 1].split('리뷰 ')[cnt])[0]

            info['mean_star'] = target.split('\n')[cnt + 3]

            while True:
                if target.split('\n')[cnt + 4] != '리뷰이미지':
                    break
                else:
                    cnt += 1

            info['star'] = target.split('\n')[cnt + 4]

            date_pattern = re.compile(r'(\d{4}.\d{2}.\d{2})')
            info['date'] = date_pattern.findall(target.split('\n')[cnt + 5])[0]

            visit_pattern = re.compile(r'\d' + '번째')
            info['visit_count'] = visit_pattern.findall(target.split('\n')[cnt + 5])[0].split('번째')[0]

        except:
            print('NoSuchElement Error')
        finally:
            self.driver.quit()
            return info

if __name__ == '__main__':
    camp_list = ['캠핑장', ' 평창 보물섬캠핑장', '서울숲']
    highlight_reviews = []  # all reviews list

    for i in range(len(camp_list)):
        s = CategoryScraping(camp_list[i])
        s.switch_iframe()
        title = s.move_tab()

        for i in range(1, 4):
            time.sleep(1)
            category = s.click_category(i)
            time.sleep(1)
            elements = s.scroll_down()

            for j, element in enumerate(elements[:3]):  # n개의 div
                info = s.get_reviews(title, category)
                highlight_reviews.append(info)

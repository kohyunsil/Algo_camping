from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import time
import pandas as pd
import camping_server2.config as config
import configparser

class OgcampScraping:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1200, 1200)
        self.driver.get("https://www.5gcamp.com/./?mod=login&iframe=Y")

    def get_data(self):
        config = configparser.ConfigParser()
        config.read('../keys/data.ini')
        ogcamp = config['API_KEYS']
        usr = ogcamp['OGCAMP_ID']
        pwd = ogcamp['OGCAMP_PW']
        id_input = self.driver.find_element_by_name('id')
        pw_input = self.driver.find_element_by_name('pw')
        submit = self.driver.find_element_by_css_selector('#btn_login')
        id_input.send_keys(usr)
        pw_input.send_keys(pwd)
        submit.click()
        time.sleep(2)

    def get_url(self):
        url_links = []
        levels = []
        for i in tqdm(range(1, 19)):
            self.driver.get(f"https://www.5gcamp.com/?c=5g&p={i}")
            items = self.driver.find_elements_by_xpath('//*[@id="camplist"]/div[2]/div[2]/div/div[2]/div')
            level = [item.find_element_by_css_selector('li.star > p').text.strip() for item in items]
            links = [item.find_element_by_css_selector('a').get_attribute('href') for item in items]
            url_links.extend(links)
            levels.extend(level)

        self.df2 = pd.DataFrame(levels)

        return url_links

    def get_details(self):
        links = self.get_url()
        datas = []
        for link in tqdm(links):
            time.sleep(1)
            self.driver.get(link)
            title = self.driver.find_element_by_css_selector('#campcontents > div.viewheader > h3').text
            addr = self.driver.find_element_by_css_selector(
                '#vContent > h4.chead.address.first.fblack > a.clipboardCopy').text

            # 위도경도 값 예외처리
            try:
                lats = self.driver.find_element_by_css_selector('#vContent > p > em').text
                lat = lats.split('경도')[0].strip()
                lon = '경도' + lats.split('경도')[1].strip()

            except NoSuchElementException:
                lats = "정보없음"
                lat = "정보없음"
                lon = "정보없음"

            envs = self.driver.find_elements_by_css_selector('#vContent > div.facilities > div > div')
            env = [env.find_element_by_css_selector("p.f_name").text for env in envs]
            en = ', '.join(env)

            try:
                desc = self.driver.find_element_by_class_name('short_cont').text
            except NoSuchElementException:
                desc = "정보없음"

            photoes = self.driver.find_elements_by_css_selector('#vContent > div.photos > div')
            photos = [photos.find_element_by_css_selector('img').get_attribute('src') for photos in photoes]
            photo = ', '.join(photos)

            # 리뷰 크롤링을 위해 스크롤 조정 후 예외처리
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            try:
                self.driver.find_element_by_xpath('//*[@id="moreComment"]/a').click
                time.sleep(1)
                reviewes = self.driver.find_elements_by_class_name('commentbox')
                reviews = [reviews.find_element_by_class_name('cont').text for reviews in reviewes]
                review = [review.replace("\n", ' ') for review in reviews]
                review = ', '.join(review)

            except NoSuchElementException:
                reviewes = self.driver.find_elements_by_class_name('commentbox')
                reviews = [reviews.find_element_by_class_name('cont').text for reviews in reviewes]
                review = [review.replace("\n", ' ') for review in reviews]
                review = ', '.join(review)

            data = {
                "title": title,
                "addr": addr,
                "lat": lat,
                "lon": lon,
                "environment": en,
                "desc": desc,
                "photo": photo,
                "review": review,
            }
            datas.append(data)

        self.df3 = pd.concat([self.df, self.df2], 1)
        self.df3.to_csv(config.PATH + '/ogcamp_scraping.csv', encoding="utf-8-sig")
        self.driver.quit()
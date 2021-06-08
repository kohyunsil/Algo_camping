from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import time
import pandas as pd
import camping_server.config as config
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


        url_links = []
        for i in tqdm(range(1,19)):
            self.driver.get(f"https://www.5gcamp.com/?c=5g&p={i}&campID=2601")
            items = self.driver.find_elements_by_xpath('//*[@id="camplist"]/div[2]/div[2]/div/div[2]/div')
            links = [item.find_element_by_css_selector('a').get_attribute('href') for item in items]
            url_links.extend(links)

        datas = []
        for link in tqdm(url_links):
            time.sleep(1)
            self.driver.get(link)
            try:
                title = self.driver.find_element_by_css_selector('#campcontents > div.viewheader > h3').text
                addr = self.driver.find_element_by_css_selector(
                    '#vContent > h4.chead.address.first.fblack > a.clipboardCopy').text
                lats = self.driver.find_element_by_css_selector('#vContent > p > em').text
                lat = lats.split('경도')[0].strip()
                lon = '경도' + lats.split('경도')[1].strip()
                envs = self.driver.find_elements_by_css_selector('#vContent > div.facilities > div > div')
                env = [env.find_element_by_css_selector("p.f_name").text for env in envs]
                en = ', '.join(env)
                desc = self.driver.find_element_by_xpath('//*[@id="vContent"]/div[6]').get_attribute('innerText')
                photoss = self.driver.find_elements_by_css_selector('#vContent > div.photos > div')
                photos = [photos.find_element_by_css_selector('img').get_attribute('src') for photos in photoss]
                photo = ', '.join(photos)
                # time.sleep(1)
                # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # click_review = self.driver.find_element_by_xpath('//*[@id="moreComment"]/a').click()
                # time.sleep(2)
                # reviews = self.driver.find_element_by_id("clist").text
            except NoSuchElementException:
                lat = "정보없음"
                lon = "정보없음"
                en = "정보없음"
                desc = "정보없음"
                photo = "정보없음"

            data = {
                "title": title,
                "addr": addr,
                "lat": lat,
                "lon": lon,
                "environment": en,
                "desc": desc,
                "photo": photo,
            }
            datas.append(data)

        self.df = pd.DataFrame(datas)
        self.df.to_csv(config.PATH + '/ogcamp.csv', encoding="utf-8-sig")
        self.driver.quit()

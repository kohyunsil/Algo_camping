import datetime
from sqlalchemy import create_engine
import pymysql
import config as config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import time
import requests
import pandas as pd
pymysql.install_as_MySQLdb()

result = []

# 신규 캠핑장에 대한 전체 리뷰 수집
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
                # print('XHR response num : ', len(response.json()['comment']['list']))  # response len 체크
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

    def to_df(self):
        kakao_reviews = pd.DataFrame()

        for r in result:
            if r == '':
                continue
            else:
                for i in r:
                    kakao_reviews = kakao_reviews.append(i, ignore_index=True)
            kakao_reviews = kakao_reviews.drop(['commentid'], axis=1)
        return kakao_reviews

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
        return self.to_df()


class Automation:
    # 데이터베이스 세팅
    def db_init(self):
        IP = config.Config.IP
        DB = config.Config.DB
        PW = config.Config.PW

        engine = create_engine(f"mysql+mysqldb://root:{PW}@{IP}/{DB}")
        conn = engine.connect()

        mydb = pymysql.connect(
            user='root',
            passwd=PW,
            host=IP,
            db=DB,
            charset='utf8',
        )
        cursor = mydb.cursor(pymysql.cursors.DictCursor)
        return engine, cursor

    # 전체 place_name, content_id 가져오기
    def select_list(self, cursor, base_ymd, cur_ymd):

        cursor.execute('select * from camping.place where modified_date between "2021-05-10" and "2021-05-30"')
        # cursor.execute('select * from camping.place where modified_date between ' + '"' + str(base_ymd) + '"' + ' and ' + '"' + str(cur_ymd) + '"')

        place_name_query = cursor.fetchall()
        place_name_df = pd.DataFrame(data=place_name_query)

        place_list = place_name_df['place_name'].tolist()
        contentid_list = place_name_df['content_id'].tolist()

        return place_list, contentid_list, place_name_df

    # place 테이블과 place_name 기준으로 merge
    def merge_raws(self, raw_df, place_df):
        # 카카오 리뷰 전처리
        proc_df = raw_df
        proc_df['platform'] = 0
        proc_df = proc_df.rename(columns={'kakaoMapUserId': 'user_id', 'point': 'star', 'likeCnt': 'like_cnt',
                                          'photoCnt': 'photo_cnt', 'username': 'user_nickname'})

        # place 테이블의 place_name 기준으로 merge
        pd.merge(proc_df, place_df, left_on='place_name', right_on='place_name', how='right')
        print(f'proc_df type : {type(proc_df)}')
        # kakao_df = proc_df.drop_duplicates()
        kakao_df = proc_df.reset_index()
        kakao_df = kakao_df.rename(columns={'index': 'id', 'userId': 'user_id', })

        kakao_df['visit_cnt'] = None
        kakao_df['mean_star'] = None
        kakao_df['review_cnt'] = None
        print(kakao_df)
        return kakao_df

    # 전체 리뷰 데이터 review table 데이터프레임 생성
    def review_table(self, kakao_df):
        review_df = kakao_df[['platform', 'user_id', 'photo_cnt', 'date', 'star', 'contents']]
        result_df = pd.DataFrame(columns=review_df.columns)

        for idx, date in enumerate(review_df['date']):
            result_df = result_df.append(review_df.iloc[idx])
        # review_df = review_df.dropna(subset=['place_id'])
        return review_df

    # reviewer table 데이터프레임 생성
    def reviewer_table(self, kakao_df):
        reviewer_df = kakao_df[['id', 'platform', 'user_nickname', 'mean_star', 'visit_cnt', 'review_cnt']]
        reviewer_df = reviewer_df.rename(columns={'id': 'review_id'})
        reviewer_df['visit_cnt'] = reviewer_df['visit_cnt'].str.split('').str[1]
        return reviewer_df

    # 데이터프레임 insert
    def insert_dataframe(self, cursor, review_df, reviewer_df):
        # sql insert
        review_df.to_sql(name='review', con=engine, if_exists='append', index=False)
        reviewer_df.to_sql(name='reviewer', con=engine, if_exists='append', index=False)

        # 제한키 설정 체크
        qry_check_one = ('''
        SET foreign_key_checks = 1;
        ''')
        cursor.execute(qry_check_one)

        # qry_fk_r = ('''
        # ALTER TABLE review
        #      ADD CONSTRAINT FK_review_place_id_place_id FOREIGN KEY (place_id)
        #         REFERENCES place (id) ON DELETE CASCADE ON UPDATE CASCADE;
        # ''')
        # cursor.execute(qry_fk_r)

        # qry_fk_rwr = ('''
        #         ALTER TABLE reviewer
        #             ADD CONSTRAINT FK_reviewer_review_id_review_id FOREIGN KEY (review_id)
        #                 REFERENCES place (id) ON DELETE CASCADE ON UPDATE CASCADE;
        #         ''')
        # cursor.execute(qry_fk_rwr)

    # 과거일 ~ 현재일 (date_range: 날짜 범위 지정)
    def calc_date(self, date_range):
        # BASEDATE = int((datetime.datetime.now() - datetime.timedelta(days=date_range)).strftime('%Y%m%d'))
        BASEDATE = str((datetime.datetime.now() - datetime.timedelta(days=date_range)).strftime('%Y-%m-%d'))
        BASEDATE = datetime.datetime.strptime(BASEDATE, '%Y-%m-%d')
        CURDATE = datetime.datetime.now()
        return BASEDATE, CURDATE


if __name__ == '__main__':
    auto = Automation()

    engine, cursor = auto.db_init()
    base_ymd, cur_ymd = auto.calc_date(45)  # 수집할 날짜 범위
    name_list, contentid_list, place_df = auto.select_list(cursor, base_ymd, cur_ymd)
    print(name_list)
    s = Scraping()
    raw_df = s.get_search(name_list)  # 크롤링 수집 완료 데이터

    kakao_df = auto.merge_raws(raw_df, place_df)  # 전처리
    review_df = auto.review_table(kakao_df)  # review 테이블 데이터프레임
    reviewer_df = auto.reviewer_table(kakao_df)  # reviewer 테이블 데이터프레임

    auto.insert_dataframe(cursor, review_df, reviewer_df)  # 데이터프레임 db에 insert
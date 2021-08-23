import kakao_reviews as kr
import datetime
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import config

pymysql.install_as_MySQLdb()

# 데이터베이스 세팅
def db_init():
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
def select_list(cursor):
    cursor.execute('SELECT content_id, place_name FROM place LIMIT 1')
    place_name_query = cursor.fetchall()
    place_name_df = pd.DataFrame(data=place_name_query)

    place_list = place_name_df['place_name'].tolist()
    contentid_list = place_name_df['content_id'].tolist()

    return place_list, contentid_list, place_name_df

# place 테이블과 place_name 기준으로 merge
def merge_raws(raw_df, place_df):
    # 카카오 리뷰 전처리
    proc_df = raw_df
    proc_df['platform'] = 0
    proc_df = proc_df.rename(columns={'kakaoMapUserId': 'user_id', 'point': 'star', 'likeCnt': 'like_cnt',
                                      'photoCnt': 'photo_cnt', 'username': 'user_nickname'})

    # place 테이블의 place_name 기준으로 merge
    pd.merge(proc_df, place_df, left_on='place_name', right_on='place_name', how='right')
    kakao_df = proc_df.drop_duplicates()
    kakao_df = kakao_df.reset_index()
    kakao_df = kakao_df.rename(columns={'index': 'id', 'userId': 'user_id', })

    kakao_df['visit_cnt'] = None
    kakao_df['mean_star'] = None
    kakao_df['review_cnt'] = None
    return kakao_df

# 기준 날짜와 비교해 review table 데이터프레임 생성
def review_table(base_ymd, kakao_df):
    review_df = kakao_df[['platform', 'user_id', 'photo_cnt', 'date', 'star', 'contents']]
    result_df = pd.DataFrame(columns=review_df.columns)

    for idx, date in enumerate(review_df['date']):
        split_date = date[:-1]
        target = datetime.datetime.strptime(split_date, '%Y.%m.%d')
        if base_ymd <= target:
            result_df = result_df.append(review_df.iloc[idx])

    # review_df = review_df.dropna(subset=['place_id'])
    return review_df

# reviewer table 데이터프레임 생성
def reviewer_table(kakao_df):
    reviewer_df = kakao_df[['id', 'platform', 'user_nickname', 'mean_star', 'visit_cnt', 'review_cnt']]
    reviewer_df = reviewer_df.rename(columns={'id': 'review_id'})
    reviewer_df['visit_cnt'] = reviewer_df['visit_cnt'].str.split('').str[1]
    return reviewer_df

# 데이터프레임 insert
def insert_dataframe(cursor, review_df, reviewer_df):
    # 제한키 설정 체크
    # qry_check_one = ('''
    # SET foreign_key_checks = 1;
    # ''')
    # cursor.execute(qry_check_one)
    #
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

    # sql insert
    review_df.to_sql(name='review', con=engine, if_exists='append', index=False)
    reviewer_df.to_sql(name='reviewer', con=engine, if_exists='append', index=False)


if __name__ == '__main__':
    engine, cursor = db_init()
    name_list, contentid_list, place_df = select_list(cursor)
    base_ymd = datetime.datetime(2021, 6, 1)

    s = kr.Scraping()
    raw_df = s.get_search(name_list)  # 크롤링 수집 완료 데이터
    kakao_df = merge_raws(raw_df, place_df)  # 전처리
    review_df = review_table(base_ymd, kakao_df)  # review 테이블 데이터프레임
    reviewer_df = reviewer_table(kakao_df)  # reviewer 테이블 데이터프레임

    insert_dataframe(cursor, review_df, reviewer_df)  # 데이터프레임 db에 insert
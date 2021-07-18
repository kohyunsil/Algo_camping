from urllib.request import Request, urlopen
import datetime
import json
from pandas.io.json import json_normalize
import xmltodict
import pandas as pd
from datetime import date
import pymysql
from sqlalchemy import create_engine

pymysql.install_as_MySQLdb()
'''
한국관광공사 관광빅데이터서비스 과거 혼잡도 (지자체) & 미래 혼잡도 예측 API 자동화 코드
API_KEY, DB 정보는 생략
'''
class KoreaTourApi:
    def __init__(self):
        self.SECRET_KEY = ''

    # 과거 혼잡도 집계
    def visitors_API(self, region_type, startYmd, endYmd):
        """
        region_type: metco(광역시), locgo(지자체)
        일자 YYMMDD 형태로 기입
        기간 내 일별 데이터 조회
        """
        url = f'http://api.visitkorea.or.kr/openapi/service/rest/DataLabService/{region_type}RegnVisitrDDList?'
        param = 'ServiceKey=' + self.SECRET_KEY + '&MobileOS=ETC&MobileApp=AppTest&numOfRows=1000000'
        detail_param = f'&startYmd={startYmd}&endYmd={endYmd}'

        request = Request(url + param + detail_param)
        request.get_method = lambda: 'GET'
        response = urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            responseData = response.read()
            rD = xmltodict.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)

            past_df = json_normalize(rDD['response']['body']['items']['item'])

            return past_df

    # 미래 혼잡도 예측 (contentId 기준)
    def tour_estiDecoAPI(self, startYmd, endYmd):
        """
        관광지별 혼잡도 예측 집계 데이터 정보 조회
        startYmd/endYmd: YYYYMMDD 양식으로 기입 (ex: 20210601)
        startYmd = endYmd 의 경우, 1일 간의 결과값 조회
        """
        url = 'http://api.visitkorea.or.kr/openapi/service/rest/DataLabService/tarDecoList?'
        param = 'ServiceKey=' + self.SECRET_KEY + '&MobileOS=ETC&MobileApp=AppTest&numOfRows=1000000'
        detail_param = f'&startYmd={startYmd}&endYmd={endYmd}'

        request = Request(url + param + detail_param)
        request.get_method = lambda: 'GET'
        response = urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            responseData = response.read()
            rD = xmltodict.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)

            future_df = json_normalize(rDD['response']['body']['items']['item'])

            return future_df

    # db cursor 생성
    def connect_sql(self, IP, DB, PW):
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

        return cursor, engine, mydb

    # 과거일 ~ 현재일 (date_range: 날짜 범위 지정)
    def calc_date(self, key, date_range):
        now = datetime.datetime.now()
        now_str = str(now.date())
        now_str = now_str.replace('-', '')
        CURDATE = int(now_str)

        if key == 0:
            BASEDATE = int((datetime.datetime.now() - datetime.timedelta(days=date_range)).strftime('%Y%m%d'))
        else:
            BASEDATE = int((datetime.datetime.now() + datetime.timedelta(days=date_range)).strftime('%Y%m%d'))

        return BASEDATE, CURDATE

    # sigungucode로 merge
    def merge_past_data(self, cursor, engine, mydb, past_df):
        # 현지인 제외
        out = past_df['touDivCd'] == '2'
        foreign = past_df['touDivCd'] == '3'
        past_df = past_df[out | foreign]
        past_api = past_df[['baseYmd', 'signguCode', 'touNum']]
        past_api = past_api.astype({'touNum': 'float'}, {'signguCode': 'int'})
        past_api = past_api.groupby(['signguCode', 'baseYmd']).sum()

        past_api = past_api.reset_index()
        past_api = past_api.rename(
            columns={'baseYmd': 'base_ymd', 'touNum': 'congestion', 'signguCode': 'sigungu_code'})
        congestion_df = past_api.dropna()

        today = date.today()
        today.isoformat()
        congestion_df['created_date'] = today.isoformat()

        # place 테이블의 sigungu_code와 merge
        cursor.execute('SELECT sigungu_code, content_id FROM place')
        place_query = cursor.fetchall()

        congestion_df = congestion_df.astype({'sigungu_code': 'int'})
        place_df = pd.DataFrame(columns=['sigungu_code', 'content_id'], data=place_query)

        merge_df = pd.merge(congestion_df, place_df, how='right', on='sigungu_code')

        return merge_df

    # content_id로 sigungucode 얻고 merge
    def merge_future_date(self, cursor, engine, mydb, esti_api):
        # place 테이블
        cursor.execute('SELECT * FROM place')
        place_query = cursor.fetchall()
        place_df = pd.DataFrame(data=place_query)

        esti_api = esti_api.astype({'contentId': 'int'})

        future = esti_api[['baseYmd', 'estiNum', 'contentId']]
        future = future.astype({'estiNum': 'float'}, {'signguCode': 'int'})
        future = future.groupby(['contentId', 'baseYmd']).sum()
        future = future.reset_index()
        future_api = future.rename(
            columns={'baseYmd': 'base_ymd', 'estiNum': 'congestion', 'contentId': 'content_id'})

        congestion_df = future_api.dropna()

        future_api = pd.merge(place_df, congestion_df, how='right', on='content_id')
        future_api = future_api[['sigungu_code', 'content_id', 'base_ymd', 'congestion']]
        future_api = future_api.fillna(0)
        future_api = future_api[future_api.sigungu_code != 0]

        future_df = future_api.astype({'sigungu_code': 'int'})

        today = date.today()
        today.isoformat()
        future_df['created_date'] = today.isoformat()

        return future_df

    # congestion 테이블 새로 생성
    def create_table(self, cursor, engine, mydb):
        drop_qry = ('''
            DROP TABLE congestion
        ''')
        cursor.execute(drop_qry)
        # sql create table
        qry29 = ('''
        CREATE TABLE congestion(
            id            INT         NOT NULL        AUTO_INCREMENT,
            sigungu_code  INT         NOT NULL,
            base_ymd      DATETIME    NOT NULL,
            created_date  DATETIME    NOT NULL,
            congestion    FLOAT       NOT NULL,
            content_id    INT         NOT NULL,
            CONSTRAINT PK_congestion PRIMARY KEY (id)
        );
        ''')
        cursor.execute(qry29)

    # db에 저장
    def save_sql(self, cursor, engine, mydb, merge_df):
        # sql insert
        merge_df.to_sql(name='congestion', con=engine, if_exists='append', index=False)



if __name__ == '__main__':
    PAST_RANGE = 20
    FUTURE_RANGE = 7
    IP = ""
    DB = ""
    PW = ""

    koreatour = KoreaTourApi()
    cursor, engine, db = koreatour.connect_sql(IP, DB, PW)

    # 과거 혼잡도 API
    BASEDATE, CURDATE = koreatour.calc_date(0, PAST_RANGE)
    past_df = koreatour.visitors_API('locgo', BASEDATE, CURDATE)
    merge_past_df = koreatour.merge_past_data(cursor, engine, db, past_df)

    # 미래 혼잡도 API
    BASEDATE, CURDATE = koreatour.calc_date(1, FUTURE_RANGE)
    future_df = koreatour.tour_estiDecoAPI(CURDATE, BASEDATE)
    merge_future_df = koreatour.merge_future_date(cursor, engine, db, future_df)

    koreatour.create_table(cursor, engine, db)

    koreatour.save_sql(cursor, engine, db, merge_past_df)  # 과거 혼잡도 insert
    koreatour.save_sql(cursor, engine, db, merge_future_df)  # 미래 혼잡도 insert

    db.close()

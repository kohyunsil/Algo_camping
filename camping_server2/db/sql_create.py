import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()


class CreateDb:
    def __init__(self):
        pass

    def create_feature_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.feature;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.feature (
                id                INT            NOT NULL   AUTO_INCREMENT, 
                content_id        INT            NOT NULL   UNIQUE, 
                place_name        TEXT           NOT NULL, 
                addr              TEXT           NOT NULL, 
                insrnc_at         VARCHAR(45)    NULL, 
                trsagnt_no        VARCHAR(45)    NULL, 
                mange             VARCHAR(45)    NULL, 
                manage_num        INT            NULL, 
                sited_stnc        INT            NULL, 
                glampinner_fclty  INT            NULL, 
                caravinner_fclty  INT            NULL, 
                trler_acmpny      VARCHAR(45)    NULL, 
                carav_acmpny      VARCHAR(45)    NULL, 
                toilet_cnt        INT            NULL, 
                swrm_cnt          INT            NULL, 
                wtrpl_cnt         INT            NULL, 
                brazier           VARCHAR(45)    NULL, 
                sbrs              INT            NULL, 
                sbrs_etc          INT            NULL, 
                posblfclty        INT            NULL, 
                extshr            INT            NULL, 
                frprvtwrpp        INT            NULL, 
                frprvtsand        INT            NULL, 
                firesensor        INT            NULL, 
                animal_cmg        VARCHAR(45)    NULL, 
                spacious_s        INT            NULL, 
                clean_s           INT            NULL, 
                hot_water_s       INT            NULL, 
                parking_s         INT            NULL, 
                with_child_s      INT            NULL, 
                ecological_s      INT            NULL, 
                cultural_s        INT            NULL, 
                festival_s        INT            NULL, 
                trail_s           INT            NULL, 
                bicycle_s         INT            NULL, 
                star_s            INT            NULL, 
                healing_s         INT            NULL, 
                with_couple_s     INT            NULL, 
                with_family_s     INT            NULL, 
                pool_s            INT            NULL, 
                valley_s          INT            NULL, 
                waterplay_s       INT            NULL, 
                pure_water_s      INT            NULL, 
                shade_s           INT            NULL, 
                ocean_s           INT            NULL, 
                extreme_s         INT            NULL, 
                with_pet_s        INT            NULL       COMMENT '(구) search 테이블에서 추가',
                price_r           INT            NULL, 
                satisfied_r       INT            NULL, 
                taste_r           INT            NULL, 
                main_r            INT            NULL, 
                object_r          INT            NULL, 
                facility_r        INT            NULL, 
                atmos_r           INT            NULL, 
                equipment_r       INT            NULL, 
                service_r         INT            NULL, 
                pool_r            INT            NULL, 
                manage_r          INT            NULL, 
                childlike_r       INT            NULL, 
                reservation_r     INT            NULL, 
                wifi_r            INT            NULL, 
                location_r        INT            NULL, 
                food_r            INT            NULL, 
                enter_r           INT            NULL, 
                view_r            INT            NULL, 
                parking_r         INT            NULL, 
                exciting_r        INT            NULL, 
                clean_r           INT            NULL, 
                conv_facility_r   INT            NULL, 
                congestion_r      INT            NULL,
                activity_m        INT            NULL      COMMENT '(구) search 테이블에서 추가', 
                nature_m          INT            NULL      COMMENT '(구) search 테이블에서 추가', 
                fun_m             INT            NULL      COMMENT '(구) search 테이블에서 추가',
                comfort_m         INT            NULL      COMMENT '(구) search 테이블에서 추가',
                together_m        INT            NULL      COMMENT '(구) search 테이블에서 추가', 
                CONSTRAINT PK_feature PRIMARY KEY (id, content_id));
                ''')
        cursor.execute(qry_result)

    def create_camp_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.camp;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.camp (
                id             INT            NOT NULL    AUTO_INCREMENT COMMENT 'Surrogate Key', 
                content_id     INT            NOT NULL    UNIQUE         COMMENT '콘텐츠ID', 
                place_name     VARCHAR(45)    NOT NULL    COMMENT '캠핑장 이름', 
                sigungu_code   INT            NOT NULL    COMMENT '국가지역코드 (5자리)', 
                addr           VARCHAR(45)    NULL        COMMENT '장소 주소', 
                lat            FLOAT          NULL        COMMENT '위도', 
                lng            FLOAT          NULL        COMMENT '경도', 
                first_image    TEXT           NULL        COMMENT '장소 대표 이미지', 
                detail_image   TEXT           NULL        COMMENT '상세이미지', 
                tel            VARCHAR(45)    NULL        COMMENT '장소 전화번호', 
                homepage       VARCHAR(45)    NULL        COMMENT '홈페이지 (고캠핑)', 
                line_intro     TEXT           NULL        COMMENT '한줄소개 (고캠핑)', 
                intro          TEXT           NULL        COMMENT '상세소개 (고캠핑)',
                tag            TEXT           NULL        COMMENT '태그', 
                readcount      INT            NULL        COMMENT '조회수', 
                animal_cmg     VARCHAR(15)    NULL        COMMENT '반려동물 동반',
                thema_envrn    VARCHAR(45)    NULL        COMMENT '테마 환경 (고캠핑)', 
                industry       VARCHAR(45)    NULL        COMMENT '업종 구분 (일반야영장, 자동차야영장 등)', 
                tour_era       VARCHAR(45)    NULL        COMMENT '여행시기 (고캠핑)', 
                oper_date      VARCHAR(45)    NULL        COMMENT '운영일', 
                oper_pd        VARCHAR(45)    NULL        COMMENT '운영기간', 
                created_date   DATETIME       NOT NULL    COMMENT '콘텐츠 최초 등록일 (고캠핑)', 
                modified_date  DATETIME       NULL        COMMENT '콘텐츠 수정일 (고캠핑)', 
                CONSTRAINT PK_place PRIMARY KEY (id, content_id)
            );
                ''')
        cursor.execute(qry_result)

    def create_tourspot_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.tourspot;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.tourspot (
                id                INT            NOT NULL    AUTO_INCREMENT COMMENT 'Surrogate Key', 
                content_id        INT            NOT NULL    UNIQUE         COMMENT '콘텐츠ID', 
                place_num         INT            NOT NULL    DEFAULT 0   COMMENT '구분 코드 (관광지 0, 축제 1)', 
                place_name        VARCHAR(45)    NOT NULL    COMMENT '장소 이름', 
                sigungu_code      INT            NOT NULL    COMMENT '국가지역코드 (5자리)', 
                addr              VARCHAR(45)    NULL        COMMENT '장소 주소', 
                lat               FLOAT          NULL        COMMENT '위도', 
                lng               FLOAT          NULL        COMMENT '경도', 
                event_start_date  DATETIME       NULL        COMMENT '축제 행사 시작일', 
                event_end_date    DATETIME       NULL        COMMENT '축제 행사 종료일', 
                first_image       TEXT           NULL        COMMENT '장소 대표 이미지', 
                readcount         INT            NULL        COMMENT '조회수',
                CONSTRAINT PK_place PRIMARY KEY (id, content_id)
            );
                ''')
        cursor.execute(qry_result)

    def create_algopoint_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.algopoint;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.algopoint (
                content_id  INT      NOT NULL    COMMENT '콘텐츠ID', 
                comfort     FLOAT    NULL        COMMENT '쾌적/편리', 
                together    FLOAT    NULL        COMMENT '함께', 
                fun         FLOAT    NULL        COMMENT '즐길거리', 
                healing     FLOAT    NULL        COMMENT '자연/힐링', 
                clean       FLOAT    NULL        COMMENT '깨끗한', 
                CONSTRAINT PK_main_cat PRIMARY KEY (content_id)
            );
                ''')
        cursor.execute(qry_result)

    def create_algotag_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.algotag;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.algotag (
                id          INT            NOT NULL    AUTO_INCREMENT COMMENT 'Surrogate Key', 
                content_id  INT            NOT NULL    COMMENT '콘텐츠ID',
                tag         VARCHAR(45)    NOT NULL    COMMENT '태그명', 
                point       FLOAT          NOT NULL    COMMENT '태그 점수', 
                CONSTRAINT PK_main_cat PRIMARY KEY (id)
            );
                ''')
        cursor.execute(qry_result)

    def create_sigungu_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.sigungu;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.sigungu (
                sigungu_code  INT            NOT NULL    COMMENT '국가지역코드 (5자리)', 
                area_name     VARCHAR(45)    NOT NULL    COMMENT '특별시, 시 이름', 
                sigungu_name  VARCHAR(45)    NOT NULL    COMMENT '시군구 이름', 
                CONSTRAINT PK_sigungucode PRIMARY KEY (sigungu_code)

            );

                ''')
        cursor.execute(qry_result)

    def create_dimension_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.dimension;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.dimension (
                id           INT            NOT NULL    AUTO_INCREMENT COMMENT '가중치 테이블 고유 아이디', 
                category     VARCHAR(45)    NOT NULL    COMMENT 'comfort, together, fun, healing, clean', 
                colname_kor  VARCHAR(45)    NOT NULL    COMMENT '태그 국문명', 
                colname      VARCHAR(45)    NOT NULL    COMMENT '태그 영문명', 
                weights      FLOAT          NULL        COMMENT '가중치', 
                tagname      VARCHAR(45)    NULL        COMMENT '고객 시각화용 태그 (버블 등)', 
                count        INT            NULL        COMMENT '고캠핑 사이트 캠핑장 개수 & 카테고리별 리뷰 개수',
                CONSTRAINT PK_weights PRIMARY KEY (id)

            );
                ''')
        cursor.execute(qry_result)

    def create_user_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.user;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.user (
                id             INT            NOT NULL    AUTO_INCREMENT COMMENT 'ID',  
                email          VARCHAR(45)    NOT NULL    UNIQUE         COMMENT '이메일', 
                name           VARCHAR(30)    NULL                       COMMENT '유저 이름', 
                password       VARCHAR(30)    NULL                       COMMENT '유저 패스워드', 
                nickname       VARCHAR(15)    NULL                       COMMENT '유저 닉네임',
                birth_date     VARCHAR(6)     NULL                       COMMENT '출생년월일 6자리 (ex:990801)',  
                created_date   DATETIME       NULL                       COMMENT '회원가입일', 
                modified_date  DATETIME       NULL                       COMMENT '수정일',
                access_token   TEXT           NULL                       COMMENT '액세스 토큰',
                A100           SMALLINT       NULL                       COMMENT '회원가입 설문 1번',
                A200           SMALLINT       NULL                       COMMENT '회원가입 설문 2번',
                A210           SMALLINT       NULL                       COMMENT '회원가입 설문 2-1번',
                A300           SMALLINT       NULL                       COMMENT '회원가입 설문 3번',
                A410           SMALLINT       NULL                       COMMENT '회원가입 설문 4-1번',
                A420           SMALLINT       NULL                       COMMENT '회원가입 설문 4-2번',
                A500           SMALLINT       NULL                       COMMENT '회원가입 설문 5번',
                A600           SMALLINT       NULL                       COMMENT '회원가입 설문 6번',
                comfort        FLOAT          NULL                       COMMENT '쾌적/편리', 
                together       FLOAT          NULL                       COMMENT '함께', 
                fun            FLOAT          NULL                       COMMENT '즐길거리', 
                healing        FLOAT          NULL                       COMMENT '자연/힐링', 
                clean          FLOAT          NULL                       COMMENT '깨끗한', 
                CONSTRAINT PK_user PRIMARY KEY (id)
            );
                ''')
        cursor.execute(qry_result)

    def create_visitor_future_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.visitor_future;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.visitor_future (
                sigungu_code  INT         NOT NULL    COMMENT '국가지역코드 (5자리)', 
                base_ymd      DATETIME    NOT NULL    COMMENT '예측 일자', 
                visitor       FLOAT       NOT NULL    COMMENT '방문객수', 
                created_date  DATETIME    NOT NULL    COMMENT '예측 모델링 실행한 일자', 
                CONSTRAINT PK_congestion PRIMARY KEY (sigungu_code, base_ymd)

            );
                ''')
        cursor.execute(qry_result)

    def create_visitor_past_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.visitor_past;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.visitor_past (
                sigungu_code  INT      NOT NULL    COMMENT '시군구코드', 
                base_ymd      DATE     NOT NULL    COMMENT '날짜',
                visitor       FLOAT    NOT NULL    COMMENT '방문객수', 
                CONSTRAINT PK_vistor_past PRIMARY KEY (sigungu_code, base_ymd)

            );
                ''')
        cursor.execute(qry_result)

    def create_sns_info_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.sns_info;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.sns_info (
                id                INT            NOT NULL    AUTO_INCREMENT COMMENT 'ID', 
                user_id           INT            NOT NULL    COMMENT '유저 ID', 
                sns_type          VARCHAR(45)    NULL        COMMENT 'sns 타입', 
                sns_id            VARCHAR(45)    NULL        COMMENT 'sns ID', 
                sns_name          VARCHAR(45)    NULL        COMMENT 'sns 이름', 
                sns_profile       VARCHAR(45)    NULL        COMMENT 'sns 프로필', 
                sns_connect_date  DATETIME       NULL        COMMENT 'sns 연결일', 
                CONSTRAINT PK_sns_info PRIMARY KEY (id, user_id)
            );
                ''')
        cursor.execute(qry_result)

    def create_review_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.review;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.review (
                id         INT            NOT NULL    AUTO_INCREMENT COMMENT '리뷰 테이블 아이디', 
                camp_id    INT            NOT NULL   				 COMMENT '캠핑장 content_id', 
                platform   INT            NOT NULL    DEFAULT 0      COMMENT '플랫폼 구분 (kakao: 0, naver: 1)', 
                user_id    VARCHAR(45)    NULL                       COMMENT '유저의 아이디 (kakao만 있음)', 
                photo_cnt  INT            NULL     					 COMMENT '사진 개수', 
                date       DATETIME       NULL     					 COMMENT '날짜', 
                cat_tag    VARCHAR(45)    NULL                       COMMENT '네이버 태그', 
                star       FLOAT          NULL                       COMMENT '별점', 
                contents   TEXT           NULL                       COMMENT '리뷰 내용', 
                CONSTRAINT PK_review PRIMARY KEY (id, camp_id)

            );
                ''')
        cursor.execute(qry_result)

    def create_user_action_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.user_action;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.user_action (
                id        INT            NOT NULL    AUTO_INCREMENT COMMENT 'Surrogate Key', 
                user_id   INT            NOT NULL    COMMENT '유저 id', 
                camp_id   INT            NOT NULL    COMMENT '캠핑장 content_id', 
                action    VARCHAR(45)    NOT NULL    COMMENT 'like, unlike, visit, unvisit', 
                datetime  TIMESTAMP      NOT NULL    COMMENT '행위 일시', 
                CONSTRAINT PK_ PRIMARY KEY (id)
            );
                ''')
        cursor.execute(qry_result)

    def create_scenario_tb(self, db, cursor):
        try:
            qry_drop = (f'''
                        drop table {db}.scenario;
                        ''')
            cursor.execute(qry_drop)
        except:
            pass

        qry_result = (f'''
            CREATE TABLE {db}.scenario (
                id              INT            NOT NULL    AUTO_INCREMENT COMMENT 'Surrogate Key', 
                scene_no        VARCHAR(4)     NOT NULL    COMMENT '유저 id', 
                content_id      INT            NOT NULL    COMMENT '캠핑장 content_id', 
                firstImageUrl   TEXT           NULL        COMMENT '첫번째 이미지', 
                spot1           SMALLINT       NOT NULL    COMMENT '상단 추천 배너 (해당:1, 비해당:0)',
                spot2           SMALLINT       NOT NULL    COMMENT '하단 롤링 배너 (해당:1, 비해당:0)', 
                CONSTRAINT PK_ PRIMARY KEY (id)
            );
                ''')
        cursor.execute(qry_result)


class Constraint:
   # 제한키 설정 체크 중지
    def fk_check_zero(self, cursor):
        qry_check_zero = ('''
        SET foreign_key_checks = 0;
        ''')
        cursor.execute(qry_check_zero)

    # 제한키 설정 체크 시작
    def fk_check_one(self, cursor):
        qry_check_one = ('''
        SET foreign_key_checks = 1;
        ''')
        cursor.execute(qry_check_one)

    def fk_algopoint_camp(self, db, cursor):
        self.fk_check_zero(cursor)
        qry_result = (f'''
        ALTER TABLE `{db}`.`algopoint` 
        ADD CONSTRAINT `fk_algopoint_camp`
          FOREIGN KEY (`content_id`)
          REFERENCES `{db}`.`camp` (`content_id`)
          ON DELETE CASCADE
          ON UPDATE CASCADE;
                ''')
        cursor.execute(qry_result)
        self.fk_check_one(cursor)

    def fk_algotag_camp(self, db, cursor):
        self.fk_check_zero(cursor)
        qry_result = (f'''
        ALTER TABLE `{db}`.`algotag` 
        ADD CONSTRAINT `fk_algotag_camp`
          FOREIGN KEY (`content_id`)
          REFERENCES `{db}`.`camp` (`content_id`)
          ON DELETE CASCADE
          ON UPDATE CASCADE;
                ''')
        cursor.execute(qry_result)
        self.fk_check_one(cursor)


class Query:
    def __init__(self):
        self.IP = ' '
        self.DB = ' '
        self.PW = ' '

    # db cursor 생성
    def connect_sql(self):
        engine = create_engine(f"mysql+mysqldb://root:{self.PW}@{self.IP}/{self.DB}?charset=utf8", encoding='utf-8')

        conn = engine.connect()

        mydb = pymysql.connect(
            user='root',
            passwd=self.PW,
            host=self.IP,
            db=self.DB,
            use_unicode=True,
            charset='utf8',
        )
        cursor = mydb.cursor(pymysql.cursors.DictCursor)
        return cursor, engine, mydb

    # db에 저장
    def save_sql(self, engine, data, table, option):
        data.to_sql(name=table, con=engine, if_exists=option, index=False)


if __name__ == '__main__':
    sql = Query()
    cursor, engine, db = sql.connect_sql()

    create = CreateDb()
    # create.create_camp_tb(sql.DB, cursor)
    # create.create_tourspot_tb(sql.DB, cursor)
    # create.create_feature_tb(sql.DB, cursor)
    # create.create_algopoint_tb(sql.DB, cursor)
    # create.create_algotag_tb(sql.DB, cursor)
    # create.create_sigungu_tb(sql.DB, cursor)
    # create.create_dimension_tb(sql.DB, cursor)
    # create.create_user_tb(sql.DB, cursor)
    # create.create_sns_info_tb(sql.DB, cursor)
    # create.create_user_action_tb(sql.DB, cursor)
    # create.create_visitor_past_tb(sql.DB, cursor)
    # create.create_visitor_future_tb(sql.DB, cursor)
    # create.create_review_tb(sql.DB, cursor)
    # create.create_scenario_tb(sql.DB, cursor)

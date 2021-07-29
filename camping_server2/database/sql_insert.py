import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
import MySQLdb

class Create():
    # db 서버 연결
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

    # db에 저장
    def save_sql(self, cursor, engine, db, data, table, option):
        data.to_sql(name=table, con=engine, if_exists=option, index=False)

    # 테이블 create
    def create_place(self, cursor):
        qry_place = ('''
        CREATE TABLE place(
            id                INT            NOT NULL     AUTO_INCREMENT,
            place_num         INT            NOT NULL, 
            place_name        TEXT           NOT NULL, 
            sigungu_code      INT            NOT NULL, 
            addr              TEXT           NULL, 
            lat               FLOAT          NULL, 
            lng               FLOAT          NULL, 
            event_start_date  DATETIME       NULL, 
            event_end_date    DATETIME       NULL, 
            first_image       TEXT           NULL, 
            second_image      TEXT           NULL, 
            tel               TEXT           NULL, 
            addr2             VARCHAR(100)   NULL, 
            thema_envrn       VARCHAR(100)   NULL, 
            tour_era          VARCHAR(45)    NULL, 
            homepage          TEXT           NULL, 
            line_intro        TEXT           NULL, 
            created_date      TEXT           NULL, 
            modified_date     TEXT           NULL, 
            detail_image      TEXT           NULL, 
            tag               TEXT           NULL, 
            readcount         INT            NULL, 
            content_id        INT            NOT NULL    UNIQUE, 
            industry          VARCHAR(45)    NULL, 
            oper_date         VARCHAR(45)    NULL, 
            oper_pd           VARCHAR(45)    NULL, 
            CONSTRAINT PK_place PRIMARY KEY (id, sigungu_code, content_id)
        );
        ''')
        cursor.execute(qry_place)

    def create_convenience(self, cursor):
        qry_convenience = ('''
        CREATE TABLE convenience(
            id                INT            NOT NULL    PRIMARY KEY    AUTO_INCREMENT, 
            place_id          INT            NOT NULL,
            sited_stnc        INT            NULL, 
            brazier           VARCHAR(45)    NULL, 
            site_bottom1      INT            NULL, 
            site_bottom2      INT            NULL, 
            site_bottom3      INT            NULL, 
            site_bottom4      INT            NULL, 
            site_bottom5      INT            NULL, 
            swrm_cnt          INT            NULL, 
            toilet_cnt        INT            NULL, 
            wtrpl_cnt         INT            NULL, 
            sbrs              TEXT           NULL, 
            sbrs_etc          TEXT           NULL, 
            eqpmn_lend        VARCHAR(45)    NULL
        );
        ''')
        cursor.execute(qry_convenience)

    def create_operation(self, cursor):
        qry_operation = ('''
        CREATE TABLE operation(
            id                INT            NOT NULL    PRIMARY KEY    AUTO_INCREMENT, 
            place_id          INT            NOT NULL, 
            mange             VARCHAR(45)    NULL,   
            manage_sttus      VARCHAR(45)    NULL, 
            prmisn_date       DATETIME       NULL, 
            faclt_div         VARCHAR(45)    NULL, 
            trsagnt_no        VARCHAR(45)    NULL, 
            mgc_div           VARCHAR(45)    NULL, 
            bizrno            VARCHAR(45)    NULL 
        );
        ''')
        cursor.execute(qry_operation)

    def create_variety(self, cursor):
        qry_variety = ('''
        CREATE TABLE variety(
            id                INT            NOT NULL    PRIMARY KEY    AUTO_INCREMENT, 
            place_id          INT            NOT NULL,
            glamp_site        INT            NULL, 
            gnrl_site         INT            NULL, 
            indvdlcarav_site  INT            NULL, 
            carav_site        INT            NULL,
            auto_site         INT            NULL, 
            carav_acmpny      VARCHAR(45)    NULL, 
            trler_acmpny      VARCHAR(45)    NULL, 
            lct               VARCHAR(45)    NULL, 
            animal_cmg        VARCHAR(45)    NULL, 
            clturevent_at     TEXT           NULL, 
            exprnprogrm_at    TEXT           NULL, 
            clturevent        TEXT           NULL, 
            posblfclty        TEXT           NULL, 
            posblfclty_etc    TEXT           NULL, 
            glampinner_fclty  VARCHAR(45)    NULL, 
            caravinner_fclty  VARCHAR(45)    NULL, 
            exprnprogrm       TEXT           NULL        
        );
        ''')
        cursor.execute(qry_variety)

    def create_safety(self, cursor):
        qry_safety = ('''
        CREATE TABLE safety(
            id                INT            NOT NULL   PRIMARY KEY     AUTO_INCREMENT, 
            place_id          INT            NOT NULL, 
            insrnc_at         VARCHAR(45)    NULL, 
            manage_num        INT            NULL, 
            extshr            INT            NULL, 
            firesensor        INT            NULL, 
            frprvtsand        INT            NULL, 
            frprvtwrpp        INT            NULL
        );
        ''')
        cursor.execute(qry_safety)
    
    def create_review(self, cursor):
        qry_review = ('''
        CREATE TABLE review(
            id          INT         NOT NULL    PRIMARY KEY     AUTO_INCREMENT,
            platform    INT         NOT NULL    DEFAULT 0, 
            user_id     VARCHAR(45) NULL, 
            place_id    INT         NOT NULL, 
            like_cnt    INT         NULL,
            photo_cnt   INT         NULL, 
            date        DATETIME    NULL, 
            cat_tag     VARCHAR(45) NULL, 
            star        FLOAT       NULL, 
            contents    TEXT        NULL
        );
        ''')
        cursor.execute(qry_review)

    def create_reviewer(self, cursor):
        qry_reviewer = ('''
        CREATE TABLE reviewer(
            id             INT            NOT NULL      PRIMARY KEY        AUTO_INCREMENT, 
            platform       INT            NOT NULL      DEFAULT 0, 
            review_id      INT            NOT NULL, 
            user_nickname  VARCHAR(45)    NULL, 
            mean_star      FLOAT          NULL, 
            visit_cnt      INT            NULL, 
            review_cnt     INT            NULL 
        );
        ''')
        cursor.execute(qry_reviewer)

    def create_search(self, cursor):
        qry_search = ('''
        CREATE TABLE search(
            id             INT           NOT NULL        PRIMARY KEY        AUTO_INCREMENT, 
            content_id     INT           NOT NULL        UNIQUE, 
            place_name     TEXT          NOT NULL, 
            addr           TEXT          NOT NULL, 
            tag            TEXT          NULL, 
            with_family_s  INT           NULL, 
            valley_s       INT           NULL, 
            clean_s        INT           NULL, 
            trail_s        INT           NULL, 
            cultural_s     INT           NULL, 
            waterplay_s    INT           NULL, 
            pure_water_s   INT           NULL, 
            ocean_s        INT           NULL, 
            with_pet_s     INT           NULL,
            star_s         INT           NULL, 
            spacious_s     INT           NULL, 
            ecological_s   INT           NULL, 
            pool_s         INT           NULL, 
            with_child_s   INT           NULL, 
            hot_water_s    INT           NULL, 
            extreme_s      INT           NULL, 
            bicycle_s      INT           NULL, 
            parking_s      INT           NULL, 
            festival_s     INT           NULL, 
            with_couple_s  INT           NULL, 
            healing_s      INT           NULL, 
            activity_m     INT           NULL, 
            nature_m       INT           NULL, 
            fun_m          INT           NULL, 
            comfort_m      INT           NULL, 
            together_m     INT           NULL 
        );
        ''')
        cursor.execute(qry_search)

    def create_algorithm(self, cursor):
        qry_algorithm = ('''
        CREATE TABLE algorithm(
            id                INT            NOT NULL   PRIMARY KEY    AUTO_INCREMENT, 
            place_name        TEXT           NULL, 
            place_id          INT            NOT NULL, 
            content_id        INT            NULL, 
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
            congestion_r      INT            NULL 
        );
        ''')
        cursor.execute(qry_algorithm)

    def create_congestion(self, cursor):
        qry_congestion = ('''
        CREATE TABLE congestion(
            id            INT         NOT NULL        PRIMARY KEY       AUTO_INCREMENT,
            sigungu_code  INT         NOT NULL, 
            base_ymd      DATETIME    NOT NULL, 
            created_date  DATETIME    NOT NULL, 
            congestion    FLOAT       NOT NULL, 
            content_id    INT         NOT NULL
        );
        ''')
        cursor.execute(qry_congestion) 

    def create_weights(self, cursor):
        qry_weights = ('''
        CREATE TABLE weights(
            id            INT            NOT NULL    PRIMARY KEY    AUTO_INCREMENT, 
            cat           VARCHAR(45)    NOT NULL, 
            original_cat  VARCHAR(45)    NOT NULL, 
            tag           VARCHAR(45)    NOT NULL, 
            tag_eng       VARCHAR(45)    NOT NULL, 
            weights       FLOAT          NULL, 
            sub_cat       VARCHAR(45)    NULL, 
            count         FLOAT          NULL
            PRIMARY KEY (id)
        );
        ''')
        cursor.execute(qry_weights)

    def create_main_cat(self, cursor):
        qry_main_cat = ('''
        CREATE TABLE main_cat(
            id          INT            NOT NULL    PRIMARY KEY      AUTO_INCREMENT, 
            content_id  INT            NOT NULL    UNIQUE, 
            place_name  VARCHAR(45)    NOT NULL, 
            comfort     FLOAT          NOT NULL, 
            together    FLOAT          NOT NULL, 
            fun         FLOAT          NOT NULL, 
            healing     FLOAT          NOT NULL, 
            clean       FLOAT          NOT NULL
            PRIMARY KEY (id)
        );
        ''')
        cursor.execute(qry_main_cat)

    def create_sigungu(self, cursor):
        qry_sigungu = ('''
        CREATE TABLE sigungucode(
            id          INT            NOT NULL    PRIMARY KEY      AUTO_INCREMENT, 
            areaCode    INT            NULL, 
            areaNm      VARCHAR(45)    NULL, 
            signguCode  INT            NULL, 
            signguNm    VARCHAR(45)    NULL
            PRIMARY KEY (id)
        );
        ''')
        cursor.execute(qry_sigungu)

# 제한키 fk 설정
class Constraint():
    # 제한키 설정 체크 중지
    def fk_check_zero (self, cursor):
        qry_check_zero = ('''
        SET foreign_key_checks = 0;
        ''')
        cursor.execute(qry_check_zero)
    
    # 제한키 설정 체크 시작
    def fk_check_one (self, cursor):
        qry_check_one = ('''
        SET foreign_key_checks = 1;
        ''')
        cursor.execute(qry_check_one)

    def fk_conveniecnce(self, cursor):
        self.fk_check_zero (cursor)
        qry_fk_c = ('''
        ALTER TABLE convenience
            ADD CONSTRAINT FK_convenience_id_place_id FOREIGN KEY (place_id)
                REFERENCES place (id) ON DELETE CASCADE ON UPDATE CASCADE;
                ''')
        cursor.execute(qry_fk_c)
        self.fk_check_one (cursor)

    def fk_operation(self, cursor):
        self.fk_check_zero (cursor)
        qry_fk_o = ('''
        ALTER TABLE operation
            ADD CONSTRAINT FK_operation_id_place_id FOREIGN KEY (place_id)
                REFERENCES place (id) ON DELETE CASCADE ON UPDATE CASCADE;
                ''')
        cursor.execute(qry_fk_o)
        self.fk_check_one (cursor)

    def fk_variety(self, cursor):
        self.fk_check_zero (cursor)
        qry_fk_v = ('''
        ALTER TABLE variety
            ADD CONSTRAINT FK_variety_id_place_id FOREIGN KEY (place_id)
                REFERENCES place (id) ON DELETE CASCADE ON UPDATE CASCADE;
        ''')
        cursor.execute(qry_fk_v)
        self.fk_check_one (cursor)    

    def fk_safety(self, cursor):
        self.fk_check_zero (cursor)
        qry_fk_s = ('''
        ALTER TABLE safety
            ADD CONSTRAINT FK_safety_id_place_id FOREIGN KEY (place_id)
                REFERENCES place (id) ON DELETE CASCADE ON UPDATE CASCADE;
        ''') 
        cursor.execute(qry_fk_s)
        self.fk_check_one (cursor) 
   
    def fk_review(self, cursor):
        self.fk_check_zero (cursor)
        qry_fk_r = ('''
        ALTER TABLE review
             ADD CONSTRAINT FK_review_place_id_place_id FOREIGN KEY (place_id)
                REFERENCES place (id) ON DELETE CASCADE ON UPDATE CASCADE;
        ''') 
        cursor.execute(qry_fk_r)
        self.fk_check_one (cursor) 

    def fk_reviewer(self, cursor):
        self.fk_check_zero (cursor)
        qry_fk_rwr = ('''
        ALTER TABLE reviewer
            ADD CONSTRAINT FK_reviewer_review_id_review_id FOREIGN KEY (review_id)
                REFERENCES place (id) ON DELETE CASCADE ON UPDATE CASCADE;
        ''') 
        cursor.execute(qry_fk_rwr)
        self.fk_check_one (cursor) 

    def fk_search(self, cursor):
        self.fk_check_zero (cursor)
        qry_fk_s = ('''
        ALTER TABLE search
            ADD CONSTRAINT FK_search_content_id_place_content_id FOREIGN KEY (content_id)
                REFERENCES place (content_id) ON DELETE CASCADE ON UPDATE CASCADE;
        ''')
        cursor.execute(qry_fk_s)
        self.fk_check_one (cursor)    

    def fk_algorithm(self, cursor):
        self.fk_check_zero (cursor)
        qry_fk_a = ('''
        ALTER TABLE algorithm
            ADD CONSTRAINT FK_algorithm_place_id_place_id FOREIGN KEY (place_id)
                REFERENCES place (id) ON DELETE CASCADE ON UPDATE CASCADE;
        ''')
        cursor.execute(qry_fk_a)
        self.fk_check_one (cursor)      

    def fk_main_cat(self, cursor):
        self.fk_check_zero (cursor)
        qry_fk_m = ('''
        ALTER TABLE main_cat
            ADD CONSTRAINT FK_main_cat_content_id_place_content_id FOREIGN KEY (content_id)
                REFERENCES place (content_id) ON DELETE CASCADE ON UPDATE CASCADE;
        ''')
        cursor.execute(qry_fk_m)
        self.fk_check_one (cursor)     


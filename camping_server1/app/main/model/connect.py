import pymysql
from sqlalchemy import create_engine
from app.config import DBConfig
pymysql.install_as_MySQLdb()

class Query:
    def __init__(self):
        self.IP = DBConfig.HOST
        self.DB = DBConfig.DB
        self.PW = DBConfig.PASSWORD

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
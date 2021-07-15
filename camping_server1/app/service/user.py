from ..model.user_dao import UserDAO as model_user
from sqlalchemy.orm import sessionmaker
from ..model import *
import datetime

# 이메일 중복 체크
def check_duplicate(param):
    email = param['email']
    param, flag = {}, False
    '''
    # select email from user where email = 'param['email']';
    '''
    Session = sessionmaker(bind=client)
    session_ = Session()
    query = session_.query(model_user).filter(model_user.email == email).all()

    param['flag'] = flag if len(query) == 0 else not flag
    param['code'] = 200
    session_.close()
    return param

# 회원가입
def get_signup(param):
    email = param['email']
    password = param['password']
    name = param['name']

    param, flag = {}, True
    '''
    # insert into user (email, name, password, created_date, modified_date) values (이메일, 패스워드, 이름);
    '''
    Session = sessionmaker(bind=client)
    session_ = Session()
    created_date = datetime.datetime.today().strftime('%Y-%m-%d 00:00:00')
    modified_date = created_date

    query = model_user(email, name, password, created_date, modified_date)
    try:
        session_.add(query)
        session_.commit()
        flag = False
    except:
        session_.rollback()
        flag = True
    finally:
        session_.close()
        param['flag'] = flag
        param['code'] = 200

        return param

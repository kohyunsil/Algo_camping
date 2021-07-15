from ..model.user_dao import UserDAO as model_user
from sqlalchemy.orm import sessionmaker
from ..model import *
import datetime
from flask_jwt_extended import *
import bcrypt
from flask import *
from app.config import Config

# 로그인 여부 확인
def is_signin():
    try:
        session['id']
        return True
    except:
        return False

# 이메일 중복 체크
def is_duplicate(param):
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
def signup(param):
    email = param['email']
    password = bcrypt.hashpw(param['password'].encode('UTF-8'), bcrypt.gensalt())
    name = param['name']

    param, flag = {}, True
    '''
    # insert into user (email, name, password, created_date, modified_date) values (이메일, 패스워드, 이름);
    '''
    Session = sessionmaker(bind=client)
    session_ = Session()
    created_date = datetime.datetime.today().strftime('%Y-%m-%d')
    modified_date = created_date

    query = model_user(email, name, password, created_date, modified_date)
    try:
        session_.add(query)
        session_.commit()
        flag = False
    except:
        session_.rollback()
        param['code'] = 500
        flag = True
    finally:
        session_.close()
        param['flag'] = flag
        param['code'] = 200

    return param

# 로그인
def signin(param):
    email = param['email']
    password = param['password']
    param = {}
    '''
    # select * from user where email = '이메일';
    '''
    try:
        query = model_user.query.filter(model_user.email == email).all()
        if len(query) == 0:
            param['access_token'] = ''
        else:
            if bcrypt.checkpw(password.encode('UTF-8'), query[0].password.encode('UTF-8')):
                email = query[0].email
                name = query[0].name

                # 암호화된 패스워드와 비교
                access_token = create_access_token(identity=email, expires_delta=Config.JWT_EXPIRATION_DELTA)
                param['access_token'] = access_token

                session['id'] = name
            else:
                param['access_token'] = ''
                param['code'] = 401
    except:
        param['code'] = 500
    else:
        param['code'] = 200

    return param

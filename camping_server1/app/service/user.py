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
        session['name']
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
    access_token = ''

    param, flag = {}, True
    '''
    # insert into user (email, name, password, access_token, created_date, modified_date) values (이메일, 패스워드, 이름);
    '''
    Session = sessionmaker(bind=client)
    session_ = Session()
    created_date = datetime.datetime.today().strftime('%Y-%m-%d')
    modified_date = created_date

    query = model_user(email, name, password, access_token, created_date, modified_date)
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
    code, access_token, name, error_msg, param = 0, '', '', '', {}
    '''
    # select * from user where email = '이메일';
    '''
    try:
        query = model_user.query.filter(model_user.email == email).all()
        if len(query) == 0:
            error_msg = '이메일을 다시 확인하세요.'
            code = 401
        else:
            # 암호화된 패스워드와 비교
            if bcrypt.checkpw(password.encode('UTF-8'), query[0].password.encode('UTF-8')):
                email = query[0].email
                name = query[0].name

                # 토큰 발급 & 저장
                Session = sessionmaker(bind=client)
                session_ = Session()

                try:
                    access_token = create_access_token(identity=email, expires_delta=Config.JWT_EXPIRATION_DELTA)
                    '''
                    # update user set access_token = access_token값 where email = email;
                    '''
                    user = session_.query(model_user).filter(model_user.email == email)[0]
                    user.access_token = access_token

                    session_.add(user)
                    session_.commit()
                except:
                    session_.rollback()
                finally:
                    session_.close()

                session.permanent = True
                app.permanent_session_lifetime = Config.SESSION_LIFETIME
                session['name'] = name
            else:
                error_msg = '비밀번호를 다시 확인하세요.'
                code = 401
    except:
        code = 500
    else:
        code = 200
    finally:
        param['code'] = code
        param['name'] = name
        param['error_msg'] = error_msg
        param['access_token'] = access_token

    return param

# 토큰 삭제
def delete_token(param):
    Session = sessionmaker(bind=client)
    session_ = Session()

    try:
        if type(param) == str:
            name = param
            '''
            # update user set access_token = null where name = 이름;
            '''
            user = session_.query(model_user).filter(model_user.name == name)[0]
            user.access_token = ''

            session_.add(user)
            session_.commit()

            session.pop('name')
        else:
            email = param['email']
            '''
            # update user set access_token = null where email = 이메일;
            '''
            user = session_.query(model_user).filter(model_user.email == email)[0]
            user.access_token = ''

            session_.add(user)
            session_.commit()
    except:
        session_.rollback()
    finally:
        session_.close()
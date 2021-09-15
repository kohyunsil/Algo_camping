from app.main.model.user_dao import UserDAO as model_user
from app.main.util.user_dto import UserDTO as user_dto
from sqlalchemy.orm import sessionmaker
from app.main.model import *
import datetime
from flask_jwt_extended import *
import bcrypt
from flask import *
from app.config import Config

# 로그인 여부 확인
def is_signin():
    param = {}
    # user getter값이 존재하는 경우
    try:
        if user_dto.user is not None:
            param = user_dto.user
        else:
            raise Exception('user_dto object is None')
    except:
        if is_exist_user():
            param = is_exist_user()
            # user getter값이 존재하지 않는 경우
            param['flag'] = True
            # setter
            user_dto.user = param
    finally:
        return param

# 유효한 토큰에 대한 유저 정보 얻기
def is_exist_user():
    try:
        if session['access_token']:
            param = {}
            '''
            # select name from user where access_token = 'access_token';
            '''
            client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
            Session = sessionmaker(bind=client)
            session_ = Session()
        try:
            query = session_.query(model_user.name).filter(model_user.access_token == session['access_token']).all()
            if len(query) == 0:
                return False
            else:
                param['name'] = query[0].name
                return param
        except:
            return False
        finally:
            session_.close()
    except:
        return False

# 이메일 중복 체크
def is_duplicate(param):
    email = param['email']
    param, flag = {}, False
    '''
    # select email from user where email = 'param['email']';
    '''
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()
    try:
        query = session_.query(model_user).filter(model_user.email == email).all()

        param['flag'] = flag if len(query) == 0 else not flag
        param['code'] = 200
    except:
        param['code'] = 500
    finally:
        session_.close()
    return param

# 회원가입
def signup(param):
    email = param['email']
    password = bcrypt.hashpw(param['password'].encode('UTF-8'), bcrypt.gensalt())
    name = param['name']
    nickname = param['nickname']
    access_token = ''

    param, flag = {}, True
    '''
    # insert into user (email, name, password, nickname, access_token, created_date, modified_date) values (이메일, 이름, 패스워드, 닉네임);
    '''
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()
    created_date = datetime.datetime.today().strftime('%Y-%m-%d')
    modified_date = created_date

    query = model_user(email, name, password, nickname, access_token, created_date, modified_date)
    try:
        session_.add(query)
        session_.commit()
        flag = False
    except:
        session_.rollback()
        param['code'] = 500
        flag = True
    finally:
        # 유저의 고유 아이디
        '''
        # select id from user where email=유저의 이메일;
        '''
        id = session_.query(model_user.id).filter(model_user.email == email).all()
        session_.close()

        param['flag'] = flag
        param['code'] = 200
        param['id'] = str(id[0][0])
        param['nickname'] = nickname

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

                client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
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
        access_token = ''
    else:
        code = 200
    finally:
        param['code'] = code
        param['name'] = name
        param['error_msg'] = error_msg
        param['access_token'] = access_token

        session['access_token'] = access_token

    return param

# 토큰 삭제
def delete_token(name):
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()
    try:
        '''
        # update user set access_token = null where name = 'name';
        '''
        user = session_.query(model_user).filter(model_user.name == name)[0]
        user.access_token = ''

        session_.add(user)
        session_.commit()

        session.pop('access_token')
        user_dto.user = None
    except:
        session_.rollback()
    finally:
        session_.close()
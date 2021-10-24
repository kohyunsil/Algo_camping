from app.main.model.user_dao import UserDAO as model_user
from app.main.util.user_dto import UserDTO as user_dto
from sqlalchemy.orm import sessionmaker
from app.main.model import *
import datetime
from flask_jwt_extended import *
import bcrypt
from flask import *
from app.config import Config
import logging
from datetime import datetime
import re
from app.main.service.user_points import UserPoints
from flask import redirect

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
            # SELECT id, email, name, nickname, birth_date FROM user WHERE access_token = 'access_token';
            '''
            client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
            Session = sessionmaker(bind=client)
            session_ = Session()
        try:
            query = session_.query(model_user.id, model_user.email, model_user.name, model_user.nickname,
                                   model_user.birth_date).filter(
                model_user.access_token == session['access_token']).all()
            if len(query) == 0:
                return False
            else:
                param['name'] = query[0].name
                param['id'] = query[0].id
                param['email'] = query[0].email
                param['nickname'] = query[0].nickname
                param['birth_date'] = query[0].birth_date

                param['access_token'] = session['access_token']
                param['code'] = 200
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
    # SELECT email FROM user WHERE email = 'param['email']';
    '''
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()
    try:
        query = session_.query(model_user).filter(model_user.email == email).all()

        param['flag'] = flag if len(query) == 0 else not flag
        logging.info('----[' + str(datetime.now()) + ' is_duplicate() : 200]----')
        param['code'] = 200
    except:
        logging.error('----[' + str(datetime.now()) + ' is_duplicate() : 500]----')
        param['code'] = 500
    finally:
        session_.close()
    return param

# 회원가입
def signup(req_email=None, req_password=None, req_name=None, req_nickname=None, req_birthDate=None):
    email = req_email
    password = bcrypt.hashpw(req_password.encode('UTF-8'), bcrypt.gensalt())
    name = req_name
    nickname = req_nickname
    birth_date = req_birthDate
    access_token = ''
    _ = ''
    member = 1

    param, flag = {}, True
    '''
    # INSERT INTO user (email, name, password, nickname, birth_date, access_token, created_date, modified_date) VALUES (이메일, 이름, 패스워드, 닉네임);
    '''
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()
    created_date = datetime.today().strftime('%Y-%m-%d')
    modified_date = created_date

    query = model_user(email, name, password, nickname, birth_date, access_token, created_date, modified_date, _,
                       _, _, _, _, _, _, _, _, _, _, _, _, _, member)
    try:
        session_.add(query)
        session_.commit()
        flag = False
    except:
        logging.error('----[' + str(datetime.now()) + ' signup() : 500]----')
        session_.rollback()
        param['code'] = 500
        flag = True
    finally:
        # 유저의 고유 아이디
        '''
        # SELECT id FROM user WHERE email = 유저의 이메일;
        '''
        id = session_.query(model_user.id).filter(model_user.email == email).all()
        session_.close()

        logging.info('----[' + str(datetime.now()) + ' signup() : 200]----')
        param['flag'] = flag
        param['code'] = 200
        param['id'] = str(id[0][0])
        param['nickname'] = nickname

    return param

# 회원가입 설문 추가
def signup_survey(param):
    survey_result = list()
    id = param['userId']
    answer1 = param['firstAnswer']
    answer2 = param['secondAnswer']
    answer2_sub = param['secondSubAnswer']
    answer3 = param['thirdAnswer']
    answer4 = param['fourthAnswer']
    answer4_sub = param['fourthSubAnswer']
    answer5 = param['fifthAnswer']
    answer6 = param['sixthAnswer']

    answer_keys = list(param.keys())
    regex = re.compile(r'Answer')

    for key in answer_keys:
        if regex.search(key):
           survey_result.append(int(param[key]))

    try:
        client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=client)
        session_ = Session()
        param = {}

        '''
        # UPDATE user SET A100 = answer1, A200 = answer2, A210 = answer2_sub, A300 = answer3, 
        # A410 = answer4, A420 = answer4_sub, A500 = answer5, A600 = answer6 WHERE id = 유저 고유 id
        '''
        user = session_.query(model_user).filter(model_user.id == id)[0]
        user.A100 = answer1
        user.A200 = answer2
        user.A210 = answer2_sub
        user.A300 = answer3
        user.A410 = answer4
        user.A420 = answer4_sub
        user.A500 = answer5
        user.A600 = answer6

        session_.add(user)
        session_.commit()
        logging.info('----[' + str(datetime.now()) + ' signup_survey() : 200]----')

        code = save_user_points(survey_result, id)['code']
        if code == 200:
            param['code'] = 200
    except:
        logging.error('----[' + str(datetime.now()) + ' signup_survey() : 500]----')
        session_.rollback()
        param['code'] = 500
    finally:
        session_.close()
    return param

# user points 저장
def save_user_points(survey_result, id):
    up = UserPoints()

    user_points = up.calc_final_point(survey_result)
    points_col = ['comfort', 'together', 'fun', 'healing', 'clean']
    user_points = {points_col[i]: point for i, point in enumerate(user_points)}

    if len(user_points) > 0:
        try:
            client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
            Session = sessionmaker(bind=client)
            session_ = Session()
            param = {}
            '''
            # UPDATE user SET comfort=유저 점수1, together=유저 점수2, fun=유저 점수3, healing=유저 점수4, clean=유저 점수5 WHERE id=유저 id;
            '''
            points_query = session_.query(model_user).filter(model_user.id == id)[0]
            points_query.comfort = user_points['comfort']
            points_query.together = user_points['together']
            points_query.fun = user_points['fun']
            points_query.healing = user_points['healing']
            points_query.clean = user_points['clean']

            session_.add(points_query)
            session_.commit()
            param['code'] = 200
            logging.info('----[' + str(datetime.now()) + ' save_user_points() : 200]----')
        except:
            logging.error('----[' + str(datetime.now()) + ' save_user_points() : 500]----')
            param['code'] = 500
        finally:
            session_.close()

        return param

# 로그인
def signin(param):
    email = param['email']
    password = param['password']
    member = ''
    code, access_token, name, error_msg, param = 0, '', '', '', {}
    '''
    # SELECT * FROM user WHERE email = '이메일';
    '''
    try:
        query = model_user.query.filter(model_user.email == email).all()
        if len(query) == 0:
            logging.warning('----[' + str(datetime.now()) + ' signin() : 401]----')
            error_msg = '이메일을 다시 확인하세요.'
            code = 401
        else:
            # 암호화된 패스워드와 비교
            if bcrypt.checkpw(password.encode('UTF-8'), query[0].password.encode('UTF-8')):
                email = query[0].email
                name = query[0].name
                member = query[0].member

                client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
                # 토큰 발급 & 저장
                Session = sessionmaker(bind=client)
                session_ = Session()

                try:
                    access_token = create_access_token(identity=email, expires_delta=Config.JWT_EXPIRATION_DELTA)
                    '''
                    # UPDATE user SET access_token = access_token값 WHERE email = email;
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
                logging.warning('----[' + str(datetime.now()) + ' signin() : 401]----')
                error_msg = '비밀번호를 다시 확인하세요.'
                code = 401
    except:
        logging.error('----[' + str(datetime.now()) + ' signin() : 500]----')
        code = 500
        access_token = ''
    else:
        logging.info('----[' + str(datetime.now()) + ' signin() : 200]----')
        code = 200
    finally:
        param['code'] = code
        param['name'] = name
        param['error_msg'] = error_msg
        param['access_token'] = access_token
        param['member'] = member

        session['access_token'] = access_token

    return param

# 정보 업데이트
def update_userinfo(param):
    email = param['email']
    password = bcrypt.hashpw(param['password'].encode('UTF-8'), bcrypt.gensalt())
    name = param['name']
    nickname = param['nickname']
    birth_date = param['birthDate']

    try:
        client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=client)
        session_ = Session()
        param = dict()
        '''
        # UPDATE user SET email = param.email, name = param.name, password = param.password, 
        # nickname = param.nickname, birth_date = param.birthdate WHERE email = param.email;
        '''
        modified_date = datetime.today().strftime('%Y-%m-%d')

        update_query = session_.query(model_user).filter(model_user.email == email)[0]
        update_query.email = email
        update_query.password = password
        update_query.name = name
        update_query.nickname = nickname
        update_query.birth_date = birth_date
        update_query.modified_date = modified_date

        session_.add(update_query)
        # 유저의 고유 아이디
        '''
        # SELECT id FROM user WHERE email = 유저의 이메일;
        '''
        id = session_.query(model_user.id).filter(model_user.email == email).all()
        session_.commit()
        param['code'] = 200
        logging.info('----[' + str(datetime.now()) + ' update_userinfo() : 200]----')
    except:
        logging.error('----[' + str(datetime.now()) + ' update_userinfo() : 500]----')
        session_.rollback()
        param['code'] = 500
    finally:
        session_.close()

    return param

# 좋아요 목록
def get_likelist():
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()

    try:
        param = dict()
        if session['access_token']:
            try:
                '''
                # SELECT like FROM user WHERE access_token = 'access token';
                '''
                like = session_.query(model_user.like).filter(model_user.access_token == session['access_token']).all()
                param['like'] = str(like[0][0])
                param['code'] = 200
                logging.info('----[' + str(datetime.now()) + ' get_likelist() : 200]----')
            except:
                logging.error('----[' + str(datetime.now()) + ' get_likelist() : 500]----')
                param['code'] = 500
            finally:
                session_.close()
    except:
        logging.error('----[' + str(datetime.now()) + ' get_likelist() : 500]----')
        param['code'] = 403
    return param

# 좋아요 업데이트
def update_like(param):
    if session['access_token'] == param['access_token']:

        like = get_likelist()['like'].split(',')
        if param['status'] == '1':
            like.append(param['content_id'])
        else:
            like.pop(like.index(param['content_id']))

        like_str = ','.join(like)

        try:
            client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
            Session = sessionmaker(bind=client)
            session_ = Session()
            param = dict()

            '''
            # UPDATE user SET like = param.content_id_list WHERE access_token = 'access_token';
            '''
            update_like_query = session_.query(model_user).filter(model_user.access_token == session['access_token'])[0]
            update_like_query.like = like_str

            session_.add(update_like_query)
            session_.commit()
            param['code'] = 200
            logging.info('----[' + str(datetime.now()) + ' update_like() : 200]----')
        except:
            logging.error('----[' + str(datetime.now()) + ' update_like() : 500]----')
            session_.rollback()
            param['code'] = 500
        finally:
            session_.close()
        return param

# 토큰 삭제
def delete_token(token):
    param = dict()
    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()
    try:
        '''
        # UPDATE user SET access_token = null WHERE access_token = token;
        '''
        user = session_.query(model_user).filter(model_user.access_token == token)[0]
        user.access_token = ''

        session_.add(user)
        session_.commit()

        session.pop('access_token')
        user_dto.user = None
        param['code'] = 200
        logging.info('----[' + str(datetime.now()) + ' delete_token() : 200]----')
    except:
        session_.rollback()
        param['code'] = 500
        logging.error('----[' + str(datetime.now()) + ' delete_token() : 500]----')
    finally:
        session_.close()
        return param

# 회원 탈퇴
def withdraw(token):
    if token == session['access_token']:
        param = dict()
        client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=client)
        session_ = Session()

        try:
            status = 0
            '''
            # UPDATE user SET member = 0 WHERE access_token = token;
            '''
            user = session_.query(model_user).filter(model_user.access_token == token)[0]
            user.member = status

            session_.add(user)
            session_.commit()

            delete_token(token)
            user_dto.user = None
            param['code'] = 200
            logging.info('----[' + str(datetime.now()) + ' withdraw() : 200]----')
        except:
            session_.rollback()
            param['code'] = 500
            logging.error('----[' + str(datetime.now()) + ' withdraw() : 500]----')
        finally:
            session_.close()
        return param

# kakao 유저 회원가입, 로그인
def social_signin(data):
    kakao_account = data.get('properties')
    email = kakao_account.get('nickname', None)
    kakao_id = str(data.get('id'))

    A100_u, A200_u, A210_u, A300_u, A410_u, A420_u, A500_u, A600_u = 0, 0, 0, 0, 0, 0, 0, 0

    client = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=client)
    session_ = Session()
    # 가입 여부 확인
    try:
        '''
        # SELECT * FROM user WHERE email = email;
        '''
        user_query = session_.query(model_user).filter(model_user.email == email).all()
        if not user_query:
            # 회원가입
            signup(email, kakao_id, email, email, None)

        # 로그인
        try:
            access_token = create_access_token(identity=email, expires_delta=Config.JWT_EXPIRATION_DELTA)
            '''
            # UPDATE user SET access_token = access_token값 WHERE email = email;
            '''
            user = session_.query(model_user).filter(model_user.email == email)[0]
            user.access_token = access_token

            session_.add(user)
            session_.commit()

            session['access_token'] = access_token

            # 유저 고유 id, 설문 내용 얻기
            '''
            # SELECT id, A100, A200, A210, A300, A410, A420, A500, A600 FROM user WHERE email = 유저의 이메일;
            '''
            query = session_.query(model_user.id).filter(model_user.email == email).all()
            id = query[0].id
            A100_u = query[0].A100
            A200_u = query[0].A200
            A210_u = query[0].A210
            A300_u = query[0].A300
            A410_u = query[0].A410
            A420_u = query[0].A420
            A500_u = query[0].A500
            A600_u = query[0].A600
        except:
            session_.rollback()
            logging.error('----[' + str(datetime.now()) + ' social_signin() line 516 : 500]----')
        finally:
            session_.close()

        session.permanent = True
        app.permanent_session_lifetime = Config.SESSION_LIFETIME
        session['name'] = email

        logging.info('----[' + str(datetime.now()) + ' social_signin() line 524 : 200]----')
    except:
        logging.error('----[' + str(datetime.now()) + ' social_signin() line 527 : 500]----')
    finally:
        session_.close()

    if A100_u == 0 and A200_u == 0 and A210_u == 0 and A300_u == 0 and A410_u == 0 and A420_u == 0 and A500_u == 0 and A600_u == 0:
        response = make_response(redirect('/signup/survey/first?id=' + str(id)))
    else:
        response = make_response(redirect('/'))

    response.set_cookie('access_token', access_token)
    response.set_cookie('id', email)

    return response
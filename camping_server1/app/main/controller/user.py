from app.main.service import user as user_service
from app.main.util.user_dto import UserDTO as user_dto
from app.main.service import main as main_service
from flask_restx import Resource, Namespace, fields
from flask import jsonify, request, session, redirect
from flask import Blueprint

user = Namespace('user', description='relating to user')
auth = Blueprint('auth', __name__, url_prefix='/auth')

user_model = user.model('User Model',
                        {'email': fields.String(required=True,
                                                description='user email'),
                         'password': fields.String(required=True,
                                                   description='user password'),
                         'name': fields.String(required=True,
                                               description='user name')
                         })

sns_user_model = user.model('SNS User Model',
                            {'name': fields.String(required=False,
                                                   description='sns user name'),
                             'email': fields.String(required=False,
                                                    description='sns user email'),
                             'profile_image': fields.String(required=False,
                                                            description='sns user profile image')
                             })


@user.route('/validation', methods=['POST'])
class UserValidation(Resource):
    validation_model = user.model('User Auth Model',
                                  {'access_token': fields.String(required=False,
                                                                 descrption='user access token')
                                   })

    @user.doc(responses={200: 'Success', 403: 'Forbidden'})
    @user.expect(validation_model)
    def post(self):
        """토큰 유효성 체크 - 추후 변경 예정인 API입니다."""
        param = {}

        values = dict(request.values)
        token = values['access_token']
        try:
            if token == session['access_token']:
                param['code'] = 200
            else:
                # 비정상적인 접근
                param['code'] = 403
        except:
            # 세션에 토큰이 만료되었거나 클라이언트에서 보낸 토큰 값이 잘못된 경우
            try:
                # getter
                param = user_dto.user
                user_service.delete_token(param['name'])
            except:
                pass
            finally:
                param['code'] = 403
        return param


@user.route('/check', methods=['POST'])
class UserCheck(Resource):
    email_check_model = user.model('User email check Model',
                                 {'email': fields.String(required=True,
                                                         description='validation check user email')})

    @user.doc(responses={400: 'Validation Error', 500: 'Database Server Error'})
    @user.response(200, 'Success', email_check_model)
    @user.expect(email_check_model)
    def post(self):
        """회원가입 중복 이메일 체크"""
        values = dict(request.values)
        return user_service.is_duplicate(values)


@user.route('/signup', methods=['POST'])
class UserSignup(Resource):
    @user.doc(responses={400: 'Validation Error', 500: 'Database Server Error'})
    @user.response(200, 'Success', user_model)
    @user.expect(user_model)
    def post(self):
        """회원가입"""
        values = dict(request.values)
        return user_service.signup(values)


@user.route('/signup/survey', methods=['GET'])
@user.doc(params={'userId': '유저 고유 아이디', 'firstAnswer': 'q1에 대한 답', 'secondAnswer': 'q2에 대한 답', 'secondSubAnswer': 'q2-1에 대한 답',
                  'thirdAnswer': 'q3에 대한 답', 'fourthAnswer': 'q4에 대한 답', 'fourthSubAnswer': 'q4-1에 대한 답',
                  'fifthAnswer': 'q5에 대한 답', 'sixthAnswer': 'q6에 대한 답'})
@user.doc(response={400: 'Validation Error', 500: 'Database Server Error'})
@user.response(200, 'Success')
class UserSurvey(Resource):
    def get(self):
        """회원가입 설문"""
        param = request.args.to_dict()
        return user_service.signup_survey(param)


@user.route('/signin', methods=['POST'])
class UserSignin(Resource):
    @user.doc(responses={400: 'Validation Error',
                         401: 'Email or Password Mismatch Error Message (이메일을 다시 확인하세요 | 비밀번호를 다시 확인하세요)',
                         500: 'Database Server Error'})
    @user.response(200, 'Success', user_model)
    @user.expect(user_model)
    def post(self):
        """로그인"""
        values = dict(request.values)
        param = user_service.signin(values)

        headers = str(request.headers)
        base_url = request.base_url
        screen = request.path
        method = request.method
        action = 'click'
        type = 'button'
        keyword = []

        main_service.user_event_logging(headers, base_url, screen, method, action, type, keyword) if param['code'] == 200 else param
        return param


@user.route('/detail', methods=['POST'])
class UserDetail(Resource):
    @user.response(200, 'Success', body=user_model)
    @user.expect(user_model)
    def post(self):
        """사용자 정보 확인 - 추후 추가할 API입니다."""
        pass


@user.route('/sns/signin', methods=['POST'])
class UserSNSSignin(Resource):
    @user.doc(responses={200: 'Success'}, body=sns_user_model)
    @user.expect(sns_user_model)
    def post(self):
        """플랫폼 로그인 - 추후 변경 예정인 API입니다."""
        values = dict(request.values)
        name = values['name']
        try:
            platform = 'kakao'
            id = values['id']  # 고유 아이디
        except:
            platform = 'naver'
            id = values['email'].split('@')[0]  # 이메일로 고유 아이디 부여

        session['name'] = name
        session['platform'] = platform
        session['id'] = id
        return jsonify({'code': 200})


@auth.route('/signout')
def signout():
    """사용자 로그아웃"""
    # getter
    user_param = user_dto.user

    headers = str(request.headers)
    base_url = request.base_url
    screen = request.path
    method = request.method
    action = 'click'
    type = 'button'
    keyword = []

    main_service.user_event_logging(headers, base_url, screen, method, action, type, keyword)
    user_service.delete_token(user_param['name'])

    return redirect(request.host_url, code=302)


@auth.route('/sns/signout')
def sns_signout():
    """플랫폼 로그아웃"""
    # getter
    param = user_dto.user
    user_service.delete_token(param['name'])
    return redirect(request.host_url, code=302)
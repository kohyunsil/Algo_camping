from app import *
from ..service import user

# @app.route('/main/protected')
# @jwt_required()
# def main_protected():
#     current_user = get_jwt_identity()
#     param = request.args.to_dict()
#     print(f'current token exist: {current_user}')
#
#     if current_user is None:
#         # 쿠키 토큰 만료
#         user.delete_token(param)
#         return render_template('index.html')
#     else:
#         # 토큰 존재
#         return render_template('index.html', param=param)

# 회원가입 중복 이메일 체크
@app.route('/user/check', methods=['POST'])
def check_email():
    values = dict(request.values)
    return user.is_duplicate(values)

# 회원가입
@app.route('/user/signup', methods=['POST'])
def save_userinfo():
    values = dict(request.values)
    return user.signup(values)

# 로그인
@app.route('/user/signin', methods=['POST'])
def login():
    values = dict(request.values)
    return user.signin(values)

# 사용자 정보 확인
@app.route('/user/detail', methods=['POST'])
@jwt_required
def user_detail():
    pass

# 로그아웃
@app.route('/user/signout')
def logout():
    user.delete_token(session['name'])
    return redirect(request.host_url, code=302)

# SNS 로그인
@app.route('/user/sns/signin', methods=['POST'])
def sns_login():
    values = dict(request.values)
    name = values['name']
    try:
        platform = 'kakao'
        id = values['id'] # 고유 아이디
    except:
        platform = 'naver'
        id = values['email'].split('@')[0] # 이메일로 고유 아이디 부여

    session['name'] = name
    session['platform'] = platform
    session['id'] = id
    return jsonify({'code': 200})

# SNS 로그아웃
@app.route('/user/sns/signout')
def sns_logout():
    session.pop('name')
    session.pop('platform')
    session.pop('id')
    return redirect('/', code=302)
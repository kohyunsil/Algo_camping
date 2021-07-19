from ..model import *
from ..service import search
from ..service import detail
from ..service import user
from app import *
from functools import wraps

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

# 검색 결과 리스트
@app.route('/search/list')
def search_tags():
    params = request.args.to_dict()
    print(params)

    if len(params) == 0 or str(list(params.keys())[0]) != 'keywords':
        return redirect('/main', code=302)
    else:
        return search.get_searchlist(params)

# 인기순 정렬
@app.route('/search/popular')
def search_popular():
    # getter
    place_obj = dto.place
    return search.get_popular_list(place_obj)

# 조회순 정렬
@app.route('/search/readcount')
def search_readcount():
    # getter
    place_obj = dto.place
    return search.get_readcount_list(place_obj)

# 등록순 정렬
@app.route('/search/recent')
def search_recent():
    # getter
    place_obj = dto.place
    return search.get_modified_list(place_obj)

# 상세 페이지
@app.route('/detail/info')
def detail_info():
    param = request.args.to_dict()
    return detail.get_detail(param)

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
    session['name'] = values['nickname']
    session['platform'] = 'kakao'
    session['id'] = values['id']
    return jsonify({'code': 200})

# SNS 로그아웃
@app.route('/user/sns/signout')
def sns_logout():
    session.pop('name')
    session.pop('platform')
    session.pop('id')
    return redirect('/', code=302)
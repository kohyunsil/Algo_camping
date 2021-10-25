from flask import *
from app.main.service import user
from app.main.service import main as main_service
from flask import Blueprint
from flask_cors import CORS, cross_origin
import flask
from ..config import Config

param = {}

route_api = Blueprint('main', __name__)

@route_api.route('/')
@route_api.route('/main')
@cross_origin()
def main_page():
    res = Response('block')
    res.headers['Access-Control-Allow-Origin'] = '*'
    param = {}

    try:
        res_param = main_service.get_swiper_banner()
        param['copy'] = res_param['copy']
        param['scene_no'] = res_param['scene_no']
        param['first_image'] = res_param['first_image']
    except:
        pass

    if user.is_signin():
        param['name'] = user.is_signin()['name']

    return render_template("index.html", param=param)


@route_api.route('/detail/<int:content_id>/<int:id>')
def detail(content_id, id):
    param = {}
    if user.is_signin():
        param['name'] = user.is_signin()['name']
    return render_template('detail.html', param=param)


@route_api.route('/signin')
def signin():
    headers = str(request.headers)
    base_url = request.base_url
    screen = request.path
    method = request.method
    action = 'click'
    type = 'button'
    keyword = []

    main_service.user_event_logging(headers, base_url, screen, method, action, type, keyword)
    return render_template('signin.html')


@route_api.route('/signup')
def signup():
    return render_template('join/signup.html')


@route_api.route('/signup/survey/first')
def survey_first():
    if user.is_signin():
        param['name'] = user.is_signin()['name']
    return render_template('join/survey1.html', param=param)


@route_api.route('/signup/survey/second')
def survey_second():
    return render_template('join/survey2.html')


@route_api.route('/signup/survey/third')
def survey_third():
    if user.is_signin():
        param['name'] = user.is_signin()['name']
    return render_template('join/survey3.html', param=param)


@route_api.route('/signup/survey/fourth')
def survey_fourth():
    if user.is_signin():
        param['name'] = user.is_signin()['name']
    return render_template('join/survey4.html', param=param)


@route_api.route('/signup/survey/fifth')
def survey_fifth():
    if user.is_signin():
        param['name'] = user.is_signin()['name']
    return render_template('join/survey5.html', param=param)


@route_api.route('/signup/survey/sixth')
def survey_sixth():
    return render_template('join/survey6.html')


@route_api.route('/signup/survey/done')
def survey_done():
    if user.is_signin():
        param['name'] = user.is_signin()['name']
    return render_template('join/done.html', param=param)


@route_api.route('/search')
@route_api.route('/search/<string:banner>/<string:scene_no>')
def search(banner=None, scene_no=None):
    if user.is_signin():
        param['name'] = user.is_signin()['name']
    return render_template('searchlist.html', param=param)


@route_api.route('/mypage')
def myinfo():
    if user.is_signin():
        param['name'] = user.is_signin()['name']
        return render_template('userinfo.html', param=param)


@route_api.route('/auth/kakao', methods=['GET', 'OPTIONS'])
@cross_origin()
def kakaoSignin():
    res = Response('block')
    res.headers['Access-Control-Allow-Origin'] = '*'

    client_id = Config.CLIENT_ID
    redirect_uri = f'{Config.BASE_URL}/auth/kakao/callback'
    kakao_oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(kakao_oauth_url, code=302)
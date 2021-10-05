from flask import *
from app.main.service import user
from app.main.service import main as main_service
from flask import Blueprint
param = {}

route_api = Blueprint('main', __name__)

@route_api.route('/')
@route_api.route('/main')
def main_page():
    param = {}
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
    return render_template('join/survey1.html')

@route_api.route('/signup/survey/second')
def survey_second():
    return render_template('join/survey2.html')

@route_api.route('/signup/survey/third')
def survey_third():
    return render_template('join/survey3.html')

@route_api.route('/signup/survey/fourth')
def survey_fourth():
    return render_template('join/survey4.html')

@route_api.route('/signup/survey/fifth')
def survey_fifth():
    return render_template('join/survey5.html')

@route_api.route('/signup/survey/sixth')
def survey_sixth():
    return render_template('join/survey6.html')

@route_api.route('/signup/survey/done')
def survey_done():
    return render_template('join/done.html')

@route_api.route('/search')
def search():
    if user.is_signin():
        param['name'] = user.is_signin()['name']
    return render_template('searchlist.html', param=param)
from flask import *
from app.main.service import user
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

@route_api.route('/detail')
def detail():
    param = {}
    if user.is_signin():
        param['name'] = user.is_signin()['name']
    return render_template('detail.html', param=param)

@route_api.route('/signin')
def signin():
    return render_template('signin.html')

@route_api.route('/signup')
def signup():
    return render_template('signup.html')

@route_api.route('/search')
def search():
    if user.is_signin():
        param['name'] = user.is_signin()['name']
    return render_template('searchlist.html', param=param)
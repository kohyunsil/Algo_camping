from flask import *
from app.main.service import user
from functools import wraps
from flask import Blueprint
param = {}

route_api = Blueprint('main', __name__)

# Authorization header token 체크
# def signin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         access_token = request.headers.get("Authorization")
#         if access_token is not None:
#             try:
#                 param = request.args.to_dict()
#             except:
#                 param = None
#         else:
#             return Response(status=401)
#
#         print(f'login_required : {param}')
#         return f(*args, **kwargs)
#
#     return decorated_function

@route_api.route('/')
@route_api.route('/main')
# @signin_required
def main_page():
    param = {}
    if user.is_signin():
        param["name"] = session["name"]
        return render_template("index.html", param=param)
    else:
        return render_template('index.html')
    # param = request.args.to_dict()
    # print(f'main page : {param}')
    # return render_template('index.html')

@route_api.route('/detail')
def detail():
    param = {}
    if user.is_signin():
        param["name"] = session["name"]
    return render_template('detail.html', param=param)

@route_api.route('/signin')
def signin():
    return render_template('signin.html')

@route_api.route('/signup')
def signup():
    return render_template('signup.html')

@route_api.route('/search')
def search():
    param = {}
    if user.is_signin():
        param["name"] = session["name"]
    return render_template('searchlist.html', param=param)
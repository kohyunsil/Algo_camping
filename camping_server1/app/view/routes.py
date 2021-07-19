from flask import *
from app import app
from app.service import user
from functools import wraps
param = {}

# Authorization header token 체크
def signin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        if access_token is not None:
            try:
                param = request.args.to_dict()
            except:
                param = None
        else:
            return Response(status=401)

        print(f'login_required : {param}')
        return f(*args, **kwargs)

    return decorated_function

@app.route('/')
@app.route('/main')
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

@app.route("/detail")
def detail():
    param = {}
    if user.is_signin():
        param["name"] = session["name"]
    return render_template('detail.html', param=param)

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/search')
def search():
    param = {}
    if user.is_signin():
        param["name"] = session["name"]
    return render_template('searchlist.html', param=param)
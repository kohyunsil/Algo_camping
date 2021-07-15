from flask import *
from app import app
from ..service import user

param = {}

@app.route('/')
@app.route('/main')
def main_page():
    if user.is_signin():
        param['name'] = session['id']
    return make_response(render_template('index.html', param=param))

@app.route("/detail")
def detail():
    if user.is_signin():
        param['name'] = session['id']
    return render_template('detail.html', param=param)

@app.route('/signin')
def signin():
    if user.is_signin():
        param['name'] = session['id']
    return render_template('signin.html', param=param)

@app.route('/signup')
def signup():
    if user.is_signin():
        param['name'] = session['id']
    return render_template('signup.html', param=param)

@app.route('/search')
def search():
    return render_template('searchlist.html', param=param)

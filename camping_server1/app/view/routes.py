from flask import *
from app import app

@app.route("/detail")
def detail():
    return render_template('detail.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/search')
def search():
    return render_template('searchlist.html')
from flask import *
from app import app

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search")
def search():
    return render_template('searchlist.html')

@app.route("/detail")
def detail():
    return render_template('detail.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')
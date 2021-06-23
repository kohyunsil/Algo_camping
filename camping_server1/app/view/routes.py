from flask import *
from app import app

# @app.route("/search/list")
# def search_list():
#     result = {'code': 200}
#     keywords = request.values.get('keywords')
#     result['keywords'] = keywords
#     print(result['keywords'])
#
#     return jsonify(result)

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

@app.route('/signup')
def signup():
    return render_template('signup.html')
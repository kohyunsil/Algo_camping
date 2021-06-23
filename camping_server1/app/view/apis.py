from flask import *
from app import app

@app.route('/search/list')
def search_list():
    result = {'code': 200}
    keywords = request.values.get('keywords')
    result['keywords'] = keywords
    print(result['keywords'])

    return jsonify(result)
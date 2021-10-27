from flask import *
from datetime import datetime
from app.main import create_app
from app import blueprint
import logging
from flask_mongoengine import MongoEngine
from flask_cors import CORS, cross_origin

app = create_app()
app.register_blueprint(blueprint)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.errorhandler(404)
def page_not_found(error):
    logging.warning('----[' + str(datetime.now()) + ' page_not_found() : 404]----')
    return redirect(url_for('main.main_page'))


@blueprint.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
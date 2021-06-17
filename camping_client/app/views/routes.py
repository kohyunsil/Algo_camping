from flask import *
from camping_client.app import app

@app.route('/')
def hello_world():
    return render_template('index.html')
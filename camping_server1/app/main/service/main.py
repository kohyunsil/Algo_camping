from flask import *
from .user import is_exist_user
import numpy as np
from app.config import Config

# 0. mysql에서 access_token이 null이 아니면 대응되는 id 가져오기
# 1. pymongo 연결
# 2. collection insert
# 3. close
# 4. return code

def save_swiper_log(param):
    if is_exist_user():
        id = is_exist_user()['id']
        position = param['id']
    else:
        id = np.random.randint(Config.RANDOM_RANGE, Config.RANDOM_RANGE * 10)

    return ''

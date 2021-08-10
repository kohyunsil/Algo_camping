from app import *
from ..service import detail

# 상세 페이지
@app.route('/detail/info')
def detail_info():
    param = request.args.to_dict()
    return detail.get_detail(param)
from app.main.service import main as main_service
from flask_restx import Resource, Namespace, fields
from flask import jsonify, request, session, redirect
from flask import Blueprint

main = Namespace('main', description='relating to main')

@main.route('/swiper', methods=['GET'])
@main.doc(params={'click_id': '클릭한 배너 id'})
@main.doc(responses={400: 'Validation Error', 500: 'Database Server Error'})
@main.response(200, 'Success')
class MainSwiper(Resource):
    def get(self):
        """메인 페이지 배너 클릭 이벤트"""
        param = request.args.to_dict()

        headers = str(request.headers)
        base_url = request.base_url
        screen = request.path
        method = request.method
        action = 'click'
        type = 'banner'
        keyword = []

        return main_service.user_event_logging(headers, base_url, screen, method, action, type, keyword, param)
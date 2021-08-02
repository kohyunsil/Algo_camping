from app.main.service import detail as detail_service
from flask_restx import Resource, Namespace
from flask import request

detail = Namespace('detail', description='relating to detail')


@detail.route('/info')
class DetailAll(Resource):
    def get(self):
        """상세 내용"""
        param = request.args.to_dict()
        return detail_service.get_detail(param)
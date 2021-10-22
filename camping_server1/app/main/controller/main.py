from app.main.service import main as main_service
from flask_restx import Resource, Namespace, fields
from flask import jsonify, request, session, redirect
from flask import Blueprint
import boto3
from botocore.client import Config
from app.config import Config as AWSConfig

main = Namespace('main', description='relating to main')

@main.route('/download/<string:file_name>', methods=['GET'])
@main.doc(params={'file_name': 'S3 요청 파일 명'})
@main.doc(responses={400: 'Validation Error', 403: 'Forbidden' , 302: 'Redirect'})
class MainResource(Resource):
    def get(self, file_name):
        """메인 페이지 이미지 리소스"""
        s3 = boto3.client('s3', config=Config(signature_version='s3v4'), region_name=AWSConfig.REGION_NAME,
                          aws_access_key_id=AWSConfig.AWS_ACCESS_KEY,
                          aws_secret_access_key=AWSConfig.AWS_SECRET_KEY)

        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': AWSConfig.BUCKET_NAME, 'Key': file_name},
                                        ExpiresIn=10000)
        return redirect(url)


@main.route('/swiper/list', methods=['GET'])
@main.doc(params={'click_id': '클릭한 배너 id'})
@main.doc(responses={400: 'Validation Error', 500: 'Database Server Error'})
@main.response(200, 'Success')
class MainSwiperList(Resource):
    def get(self):
        """메인 페이지 배너 클릭에 대한 리스트"""
        param = request.args.to_dict()

        headers = str(request.headers)
        base_url = request.base_url
        screen = request.path
        method = request.method
        action = 'click'
        type = 'banner'
        keyword = []

        return main_service.user_event_logging(headers, base_url, screen, method, action, type, keyword, param)


@main.route('/swiper/recommend/<int:refresh>', methods=['GET'])
@main.doc(response={400: 'Validation Error', 500: 'Database Server Error'})
@main.response(200, 'Success')
class MainSwiperRecommend(Resource):
    def get(self, refresh):
        """추천 배너"""
        param = request.args.to_dict()

        # 로그인 ㅇ
        try:
            if session['access_token'] == param['access_token']:
                param = main_service.get_user_recommend_swiper(param)
                if refresh == 0:
                    # 최초 로그인 후 메인화면 진입 시
                    init_copy = '어..? ' + session['name'] + '님 이런 캠핑장 좋아하실거 같아요..!'
                    param['copy'] = init_copy

                param['name'] = session['name']
                return param
        # 로그인 x
        except:
            return main_service.get_recommend_swiper()


@main.route('/swiper/banner', methods=['GET'])
@main.doc(response={400: 'Validation Error', 500: 'Database Server Error'})
@main.response(200, 'Success')
class MainSwiperRecommend(Resource):
    def get(self):
        """swiper 배너"""
        return main_service.get_swiper_banner()

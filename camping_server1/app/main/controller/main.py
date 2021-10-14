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
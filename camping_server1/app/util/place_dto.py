from flask_restx import Namespace, fields
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, Float, DateTime

class PlaceDTO(object):
    # api = Namespace('place', description='relating to place')
    # place = api.model('place', {
    #     'place_name': fields.String(required=False),
    #     'content_id': fields.Integer(required=False),
    #     'sigungu_code': fields.Integer(required=False),
    #     'addr': fields.String(required=False),
    #     'lat': fields.Float(required=False),
    #     'lng': fields.Float(required=False),
    #     'event_start_date': fields.DateTime(required=False),
    #     'event_end_date': fields.DateTime(required=False),
    #     'first_image': fields.String(required=False),
    #     'second_image': fields.String(required=False),
    #     'detail_image': fields.String(required=False),
    #     'tel': fields.String(required=False),
    #     'tag': fields.String(required=False),
    #     'homepage': fields.String(required=False),
    #     'line_intro': fields.String(required=False),
    # })

    @hybrid_property
    def place(self):
        print('getter of place called!')
        return self.place_obj

    @place.setter
    def place(self, place_obj):
        self.place_obj = place_obj
        print('setter of place called!')



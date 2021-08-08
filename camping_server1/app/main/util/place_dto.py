from sqlalchemy.ext.hybrid import hybrid_property
from flask_restx import Namespace, fields


class PlaceDTO(object):
    # api = Namespace('place', description='relating to place info')

    @hybrid_property
    def place(self):
        return self.place_obj

    @place.setter
    def place(self, place_obj):
        self.place_obj = place_obj

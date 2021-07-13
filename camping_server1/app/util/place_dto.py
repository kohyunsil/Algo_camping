from sqlalchemy.ext.hybrid import hybrid_property


class PlaceDTO(object):
    @hybrid_property
    def place(self):
        return self.place_obj

    @place.setter
    def place(self, place_obj):
        self.place_obj = place_obj



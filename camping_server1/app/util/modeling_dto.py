from sqlalchemy.ext.hybrid import hybrid_property


class ModelingDTO(object):
    @hybrid_property
    def modeling(self):
        return self.algo_info

    @modeling.setter
    def modeling(self, algo_info):
        self.algo_info = algo_info
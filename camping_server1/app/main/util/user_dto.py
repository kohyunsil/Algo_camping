from sqlalchemy.ext.hybrid import hybrid_property


class UserDTO(object):

    @hybrid_property
    def user(self):
        return self.user_obj

    @user.setter
    def user(self, user_obj):
        self.user_obj = user_obj
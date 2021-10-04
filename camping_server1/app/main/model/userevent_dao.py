from flask_mongoengine.wtf import model_form
from ..model import mongodb
import datetime

class Param(mongodb.EmbeddedDocument):
    type = mongodb.StringField()
    position = mongodb.StringField()
    keyword = mongodb.ListField()


class UserEventDAO(mongodb.Document):
    meta = {'collection': 'userEvent'}

    isSignin = mongodb.IntField(max_length=2)
    userNo = mongodb.IntField()
    date = mongodb.DateTimeField(default=datetime.datetime.now)
    screen = mongodb.StringField()
    action = mongodb.StringField()

    param = mongodb.EmbeddedDocumentField(Param)
from mongoengine import *

class Checkin(DynamicDocument):
    pass

class LatestCheckin(Document):
    user_id = IntField()
    checkin = ReferenceField(Checkin)

class Visit(Document):
    username = StringField()
    when = DateTimeField()
    checkin = ReferenceField(Checkin)

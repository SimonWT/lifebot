from .db import db

class Place(db.Document):
    name = db.StringField(required=True, unique=False)
    country =  db.StringField(required=True, unique=False)
    city =  db.StringField(required=True, unique=False)
    address =  db.StringField(required=False, unique=False)
    lat = db.FloatField(required=True)
    lon = db.FloatField(required=True)

class Review(db.Document):
    chat_id = db.StringField(required=True, unique=False)
    content = db.StringField(required=True, unique=False)
    place = db.ReferenceField(Place)

class User(db.Document):
    chat_id = db.StringFiled(required=True, unique=True)
    
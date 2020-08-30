from .db import db

class Place(db.Document):
    name = db.StringField(required=True, unique=False)
    country =  db.StringField(required=True, unique=False)
    city =  db.StringField(required=True, unique=False)
    address =  db.StringField(required=False, unique=False)

class Review(db.Document):
    chat_id = db.StringField(required=True, unique=False)
    
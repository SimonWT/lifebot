from .db import db

class User(db.Document):
    chat_id = db.LongField(required=True, unique=True)
    name = db.StringField()
    gender = db.StringField()
    age = db.StringField()

### Where to Go ###

class Place(db.Document):
    name = db.StringField(required=True, unique=False)
    country = db.StringField(required=True, unique=False)
    city = db.StringField(required=True, unique=False)
    address = db.StringField(required=False, unique=False)
    lat = db.FloatField(required=True)
    lon = db.FloatField(required=True)

class Review(db.Document):
    chat_id = db.StringField(required=True, unique=False)
    content = db.StringField(required=True, unique=False)
    place = db.ReferenceField(Place)

### Money Part ###

class Wallet(db.Document):
    user = db.ReferenceField(User)
    balance = db.FloatField(required=True)

class Transaction(db.Document):
    wallet = db.ReferenceField(Wallet, unique=False)
    category = db.StringField()
    delta = db.FloatField(required=True)
    time = db.DateTimeField(required=True)
from flask import Blueprint, Response
from database.models import Place

places = Blueprint('places', __name__)


@places.route('/api/places', methods=['GET'])
def get_places():
    places = Place.objects().to_json()
    return Response(places, mimetype="application/json", status=200)

@places.route('/api/places', methods=['POST'])
def add_place():
    body = request.get_json()
    place = Place(**body).save()
    id = place.id
    return {'id': str(id)}, 200

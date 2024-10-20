from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from places.models import Place


def serialize_places(places: list):
    return {
        "type": "FeatureCollection",
        "features": places
    }


def serialize_place(place: Place):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [place.longitude, place.latitude]
        },
        "properties": {
            "title": place.title,
            "placeId": place.id,
            "detailsUrl": reverse('place_detail', args=[place.id])
        }
    }


def serialize_place_json(place: Place):
    return {
        "title": place.title,
        "imgs": [object.image.url for object in place.images.all()],
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {
            "lat": place.latitude,
            "lng": place.longitude
        }
    }


def show_index(request):
    places = []
    db_places = Place.objects.all()
    for place in db_places:
        places.append(serialize_place(place))
    context = {
        "geojson": serialize_places(places)
    }
    return render(request, 'index.html', context)


def get_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    return JsonResponse(serialize_place_json(place))

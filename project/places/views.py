from django.shortcuts import render
from places.models import Place
import json
from django.core.serializers import serialize
from django.http import HttpResponse, HttpRequest, JsonResponse

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
            "coordinates": [place.coordinates_lng, place.coordinates_lat]
        },
            "properties": {
            "title": place.title,
            "placeId": place.id,
            "detailsUrl": f"./places/{place.id}"
            }
    }

def serialize_place_json(place: Place):
    return {
        "title": place.title,
        "imgs": [object.image.url for object in place.images.all()],
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates":{
            "lat": place.coordinates_lat,
            "lng": place.coordinates_lng            
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
    print(context)
    return render(request, 'index.html', context)


def get_place(request, place_id):
   # print(place_id)
    place = Place.objects.get(id=place_id)
    #print(place.images)
    
    return JsonResponse(serialize_place_json(place))

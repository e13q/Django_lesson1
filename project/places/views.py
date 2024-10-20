from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from places.models import Place


def show_index(request):
    places = []
    db_places = Place.objects.all()
    for place in db_places:
        places.append(
            {
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
        )
    context = {
        "geojson": {
            "type": "FeatureCollection",
            "features": places
        }
    }
    return render(request, 'index.html', context)


def get_place(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related('images'), id=place_id
    )
    return JsonResponse(
        {
            "title": place.title,
            "imgs": [object.image.url for object in place.images.all()],
            "description_short": place.short_description,
            "description_long": place.long_description,
            "coordinates": {
                "lat": place.latitude,
                "lng": place.longitude
            }
        }
    )

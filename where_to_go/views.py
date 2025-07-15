from django.shortcuts import render
from django.urls import reverse

from places.models import Place


def get_places_map(request):
    """Получает данные всех мест из БД и отображает карту с метками"""
    places_geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    places = Place.objects.all()
    for place in places:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(place.longitude), float(place.latitude)]
            },
            "properties": {
                "title": place.title,
                "placeId": str(place.id),
                "detailsUrl": reverse('place_details', kwargs={'place_id': place.id})
            }
        }
        places_geojson["features"].append(feature)
    
    return render(request, 'index.html', {
        'places_geojson': places_geojson
    })
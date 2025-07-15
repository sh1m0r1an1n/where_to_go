import urllib.parse

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Place


def get_places_map(request):
    """Получает данные всех мест из БД и отображает карту с метками"""
    places_geojson = {
        'type': 'FeatureCollection',
        'features': []
    }
    
    places = Place.objects.all()
    for place in places:
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(place.longitude), float(place.latitude)]
            },
            'properties': {
                'title': place.title,
                'placeId': str(place.id),
                'detailsUrl': reverse('place_details', kwargs={'place_id': place.id})
            }
        }
        places_geojson['features'].append(feature)
    
    return render(request, 'index.html', {
        'places_geojson': places_geojson
    })


def get_place_details_json(request, place_id):
    """Возвращает JSON данные о конкретном месте по его ID"""
    place = get_object_or_404(
        Place.objects.prefetch_related('images'), 
        id=place_id
    )
    
    image_urls = [
        urllib.parse.unquote(image.image.url) 
        for image in place.images.all() 
        if image.image
    ]
    
    serialized_place = {
        'title': place.title,
        'imgs': image_urls,
        'description_short': place.short_description,
        'description_long': place.long_description,
        'coordinates': {
            'lng': str(place.longitude),
            'lat': str(place.latitude)
        }
    }
    
    return JsonResponse(
        serialized_place,
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 2
        }
    )

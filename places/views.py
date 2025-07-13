from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Place


def get_place_details_json(request, place_id):
    """Возвращает JSON данные о конкретном месте по его ID"""
    place = get_object_or_404(Place, id=place_id)
    
    images = place.images.all()
    
    response_data = {
        'title': place.title,
        'imgs': [image.image.url for image in images],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': str(place.longitude),
            'lat': str(place.latitude)
        }
    }
    
    return JsonResponse(response_data)

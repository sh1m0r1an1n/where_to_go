from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Place
import urllib.parse


def get_place_details_json(request, place_id):
    """Возвращает JSON данные о конкретном месте по его ID"""
    place = get_object_or_404(Place, id=place_id)
    
    image_urls = []
    for image in place.images.all():
        if image.image:
            decoded_url = urllib.parse.unquote(image.image.url)
            image_urls.append(decoded_url)
    
    response_data = {
        'title': place.title,
        'imgs': image_urls,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': str(place.longitude),
            'lat': str(place.latitude)
        }
    }
    
    return JsonResponse(
        response_data,
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 2
        }
    )

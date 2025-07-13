import json
import os
from urllib.parse import urlparse
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.db import transaction
import requests
from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Загружает данные о месте из JSON файла или URL'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_source',
            type=str,
            help='URL или путь к JSON файлу с данными о месте'
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перезаписать данные места, если оно уже существует'
        )

    def handle(self, *args, **options):
        json_source = options['json_source']
        force = options['force']
        
        try:
            if json_source.startswith(('http://', 'https://')):
                place_data = self._load_from_url(json_source)
            else:
                place_data = self._load_from_file(json_source)
                
            self._load_place_data(place_data, force)
            
        except Exception as e:
            raise CommandError(f'Ошибка загрузки данных: {e}')

    def _load_from_url(self, url):
        """Загружает JSON данные из URL"""
        self.stdout.write(f'Загрузка данных из URL: {url}')
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise CommandError(f'Ошибка загрузки из URL: {e}')
        except json.JSONDecodeError as e:
            raise CommandError(f'Ошибка парсинга JSON: {e}')

    def _load_from_file(self, file_path):
        """Загружает JSON данные из локального файла"""
        self.stdout.write(f'Загрузка данных из файла: {file_path}')
        
        if not os.path.exists(file_path):
            raise CommandError(f'Файл не найден: {file_path}')
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise CommandError(f'Ошибка парсинга JSON файла: {e}')

    def _load_place_data(self, place_data, force):
        """Загружает данные о месте в базу данных"""
        required_fields = ['title', 'description_short', 'description_long', 'coordinates']
        for field in required_fields:
            if field not in place_data:
                raise CommandError(f'Отсутствует обязательное поле: {field}')
        
        coordinates = place_data['coordinates']
        if 'lat' not in coordinates or 'lng' not in coordinates:
            raise CommandError('Отсутствуют координаты (lat, lng)')
        
        title = place_data['title']
        
        with transaction.atomic():
            place, created = Place.objects.get_or_create(
                title=title,
                defaults={
                    'description_short': place_data['description_short'],
                    'description_long': place_data['description_long'],
                    'latitude': coordinates['lat'],
                    'longitude': coordinates['lng']
                }
            )
            
            if not created and not force:
                self.stdout.write(
                    self.style.WARNING(f'Место "{title}" уже существует. Используйте --force для перезаписи.')
                )
                return
            
            if not created and force:
                place.description_short = place_data['description_short']
                place.description_long = place_data['description_long']
                place.latitude = coordinates['lat']
                place.longitude = coordinates['lng']
                place.save()
                
                place.images.all().delete()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Место "{title}" обновлено.')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Место "{title}" создано.')
                )
            
            if 'imgs' in place_data:
                self._load_place_images(place, place_data['imgs'])

    def _load_place_images(self, place, image_urls):
        """Загружает изображения для места"""
        self.stdout.write(f'Загрузка {len(image_urls)} изображений...')
        
        for order, image_url in enumerate(image_urls):
            try:
                self._download_and_save_image(place, image_url, order)
                self.stdout.write(f'  Загружено изображение {order + 1}/{len(image_urls)}')
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  Ошибка загрузки изображения {image_url}: {e}')
                )

    def _download_and_save_image(self, place, image_url, order):
        """Скачивает и сохраняет изображение"""
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            parsed_url = urlparse(image_url)
            filename = os.path.basename(parsed_url.path)
            
            if not filename:
                filename = f'image_{order}.jpg'
            
            place_image = PlaceImage(place=place, order=order)
            
            place_image.image.save(
                filename,
                ContentFile(response.content),
                save=True
            )
            
        except requests.RequestException as e:
            raise Exception(f'Ошибка скачивания изображения: {e}')
        except Exception as e:
            raise Exception(f'Ошибка сохранения изображения: {e}') 
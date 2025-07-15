import os

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def place_image_path(instance, filename):
    """Генерирует путь для сохранения изображения места"""
    place_id = instance.place.id
    return os.path.join('places', f'place_{place_id}', filename)


class Place(models.Model):
    """Модель для хранения информации о местах"""
    
    title = models.CharField(max_length=200, verbose_name='Название места')
    short_description = models.TextField(verbose_name='Краткое описание', blank=True)
    long_description = models.TextField(verbose_name='Подробное описание', blank=True)
    
    latitude = models.DecimalField(
        max_digits=16,
        decimal_places=14,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ],
        verbose_name='Широта'
    )
    
    longitude = models.DecimalField(
        max_digits=16,
        decimal_places=14,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ],
        verbose_name='Долгота'
    )
    
    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ['title']
    
    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    """Модель для хранения изображений мест"""
    
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
    )
    
    image = models.ImageField(
        upload_to=place_image_path,
        verbose_name='Изображение'
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
        help_text='Порядок отображения изображения (заполняется автоматически)'
    )
    
    class Meta:
        verbose_name = 'Изображение места'
        verbose_name_plural = 'Изображения мест'
        ordering = ['place', 'order']
        indexes = [
            models.Index(fields=['place', 'order'], name='place_order_idx'),
        ]
    
    def __str__(self):
        return f"Изображение {self.order} для {self.place.title}"
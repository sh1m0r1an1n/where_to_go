from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Place(models.Model):
    """Модель для хранения информации о местах"""
    
    title = models.CharField(max_length=200, verbose_name="Название места")
    description_short = models.TextField(verbose_name="Краткое описание")
    description_long = models.TextField(verbose_name="Подробное описание")
    
    latitude = models.DecimalField(
        max_digits=16,
        decimal_places=14,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ],
        verbose_name="Широта"
    )
    
    longitude = models.DecimalField(
        max_digits=16,
        decimal_places=14,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ],
        verbose_name="Долгота"
    )
    
    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        ordering = ['title']
    
    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    """Модель для хранения изображений мест"""
    
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Место"
    )
    
    image_url = models.URLField(max_length=500, verbose_name="URL изображения")
    
    class Meta:
        verbose_name = "Изображение места"
        verbose_name_plural = "Изображения мест"
        ordering = ['place', 'id']
    
    def __str__(self):
        return f"Изображение для {self.place.title}"
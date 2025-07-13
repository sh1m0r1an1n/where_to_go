from django.contrib import admin
from django.utils.html import format_html
from .models import Place, PlaceImage
import traceback


class PlaceImageInline(admin.TabularInline):
    """Inline для отображения изображений места в админке"""
    
    model = PlaceImage
    extra = 1
    fields = ['image', 'image_preview', 'order']
    readonly_fields = ['image_preview']
    ordering = ['order']
    
    def image_preview(self, obj):
        """Показывает превью изображения в inline форме"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px; object-fit: contain;" />',
                obj.image.url
            )
        return "Изображение не загружено"
    
    image_preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """Админка для модели Place"""
    
    list_display = [
        'title', 
        'latitude', 
        'longitude',
        'images_count'
    ]
    
    search_fields = ['title', 'description_short', 'description_long']
    
    fields = [
        'title',
        'description_short', 
        'description_long',
        'latitude',
        'longitude'
    ]
    
    inlines = [PlaceImageInline]
    
    def images_count(self, obj):
        """Показывает количество изображений для места"""
        try:
            count = obj.images.count()
            return f"{count} изображений"
        except Exception as e:
            print(f"Ошибка в images_count: {e}")
            print(traceback.format_exc())
            return "Ошибка подсчета"
    
    images_count.short_description = "Изображения"


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    """Админка для модели PlaceImage"""
    
    list_display = [
        'place', 
        'order',
        'image_preview'
    ]
    
    list_filter = ['place']
    
    search_fields = ['place__title']
    
    ordering = ['place', 'order']
    
    fields = [
        'place',
        'image',
        'image_preview',
        'order'
    ]
    
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """Показывает превью изображения"""
        try:
            if obj.image:
                return format_html(
                    '<img src="{}" style="max-height: 200px; max-width: 400px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" />',
                    obj.image.url
                )
            return "Нет изображения"
        except Exception as e:
            # Выводим ошибку в консоль для отладки
            print(f"Ошибка в image_preview: {e}")
            print(traceback.format_exc())
            return "Ошибка загрузки превью"
    
    image_preview.short_description = "Превью"
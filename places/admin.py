from django.contrib import admin
from django.utils.html import format_html
from .models import Place, PlaceImage


class PlaceImageInline(admin.TabularInline):
    """Inline для отображения изображений места в админке"""
    
    model = PlaceImage
    extra = 1
    fields = ['image', 'order']
    ordering = ['order']


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
    
    inlines = [PlaceImageInline]
    
    def images_count(self, obj):
        """Показывает количество изображений для места"""
        count = obj.images.count()
        return f"{count} изображений"
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
    
    def image_preview(self, obj):
        """Показывает превью изображения"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = "Превью"
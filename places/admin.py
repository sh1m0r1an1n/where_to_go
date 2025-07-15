from django.contrib import admin
from django.utils.html import format_html

from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from tinymce.widgets import TinyMCE

from .models import Place, PlaceImage


class PlaceImageInline(SortableTabularInline):
    """Inline для отображения изображений места в админке с поддержкой сортировки"""
    
    model = PlaceImage
    extra = 0
    fields = ['image', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """Показывает превью изображения в inline форме"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px; object-fit: contain;" />',
                obj.image.url
            )
        return 'Изображение не загружено'
    
    image_preview.short_description = 'Превью'


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    """Админка для модели Place"""
    
    list_display = [
        'title', 
        'latitude', 
        'longitude',
        'images_count'
    ]
    
    search_fields = ['title', 'short_description', 'long_description']
    
    fields = [
        'title',
        'short_description', 
        'long_description',
        'latitude',
        'longitude'
    ]
    
    inlines = [PlaceImageInline]
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Настройка виджетов для полей"""
        if db_field.name == 'long_description':
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30})
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    def images_count(self, obj):
        """Показывает количество изображений для места"""
        count = obj.images.count()
        return f'{count} изображений'
    
    images_count.short_description = 'Изображения'


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
    
    autocomplete_fields = ['place']
    
    fields = [
        'place',
        'image',
        'image_preview'
    ]
    
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """Показывает превью изображения"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 400px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" />',
                obj.image.url
            )
        return 'Нет изображения'
    
    image_preview.short_description = 'Превью'
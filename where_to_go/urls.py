from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from where_to_go import views
from places import views as places_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.get_places_map, name='main'),
    path('places/<int:place_id>/', places_views.get_place_details_json, name='place_details'),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

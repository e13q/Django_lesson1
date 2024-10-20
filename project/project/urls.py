from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from places.views import show_index, get_place

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_index),
    path('places/<int:place_id>/', get_place, name='place_detail'),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

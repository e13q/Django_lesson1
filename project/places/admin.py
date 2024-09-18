from django.contrib import admin
from places.models import Image, Coordinates, Place


admin.site.register(Place)
admin.site.register(Coordinates)
admin.site.register(Image)